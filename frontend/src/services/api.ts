import axios from 'axios';
import type {
  SourcePlate,
  PlateLayout,
  PicklistEntry,
  LayoutRequest,
  UpdateLayoutRequest,
  ChatRequest,
} from '../types';

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
});

// 文件解析
export async function parseFile(file: File): Promise<SourcePlate> {
  const formData = new FormData();
  formData.append('file', file);
  const response = await api.post('/file/parse', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  
  // 转换后端格式到前端格式
  const data = response.data;
  const wells = (data.wells || []).map((w: { position: string; gene_symbol: string; volume?: number; concentration?: number }) => ({
    wellId: w.position,
    geneId: w.gene_symbol,
    geneName: w.gene_symbol,
    volume: w.volume || 100,
    concentration: w.concentration || 0,
  }));
  
  // 计算唯一基因数
  const uniqueGenes = new Set(wells.map((w: { geneId: string }) => w.geneId));
  
  return {
    plateId: data.barcode || 'UNKNOWN',
    wells,
    totalGenes: uniqueGenes.size,
    totalVolume: wells.reduce((sum: number, w: { volume: number }) => sum + (w.volume || 0), 0),
  };
}

// 布局生成
export async function generateLayout(request: LayoutRequest): Promise<PlateLayout> {
  const response = await api.post<PlateLayout>('/layout/generate', request);
  return response.data;
}

// 布局更新
export async function updateLayout(request: UpdateLayoutRequest): Promise<PlateLayout> {
  const response = await api.put<PlateLayout>('/layout/update', request);
  return response.data;
}

// 生成 Picklist
export async function generatePicklist(layout: PlateLayout, sourcePlate: SourcePlate): Promise<PicklistEntry[]> {
  // 转换前端格式到后端格式
  const backendLayout = {
    plate_barcode: layout.layoutId,
    plate_type: layout.plateFormat,
    plate_index: 0,
    wells: layout.wells.map(w => ({
      position: w.wellId,
      row: w.row,
      col: w.col,
      content_type: w.wellType,
      gene_symbol: w.geneId,
      replicate_index: w.replicateIndex,
      source_plate: sourcePlate.plateId,
      source_well: sourcePlate.wells.find(sw => sw.geneId === w.geneId)?.wellId
    }))
  };
  
  const backendSourcePlate = {
    barcode: sourcePlate.plateId,
    plate_type: "384PP_AQ_BP",
    wells: sourcePlate.wells.map(w => ({
      position: w.wellId,
      gene_symbol: w.geneId,
      volume: w.volume
    }))
  };
  
  const response = await api.post('/layout/picklist', {
    layouts: [backendLayout],
    source_plate: backendSourcePlate,
    transfer_volume: 2500  // 默认 2.5ul = 2500nL
  });
  
  // 转换后端格式到前端格式
  const entries = response.data.entries || [];
  return entries.map((e: {
    source_plate_barcode: string;
    source_well: string;
    destination_plate_barcode: string;
    destination_well: string;
    transfer_volume: number;
    gene_symbol: string;
  }) => ({
    sourceBarcode: e.source_plate_barcode,
    sourceWell: e.source_well,
    destBarcode: e.destination_plate_barcode,
    destWell: e.destination_well,
    volume: e.transfer_volume,
    geneId: e.gene_symbol,
    geneName: e.gene_symbol
  }));
}

// SSE 聊天流
export function createChatStream(
  request: ChatRequest,
  onMessage: (text: string) => void,
  onLayout: (layout: PlateLayout) => void,
  onError: (error: string) => void,
  onDone: () => void
): () => void {
  const controller = new AbortController();

  fetch('/api/chat/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request),
    signal: controller.signal,
  })
    .then(async (response) => {
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      const reader = response.body?.getReader();
      if (!reader) throw new Error('No reader');

      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6).trim();
            if (!data) continue;
            
            try {
              const event = JSON.parse(data);
              if (event.type === 'text' && event.content) {
                onMessage(event.content);
              } else if (event.type === 'layout' && event.content) {
                onLayout(event.content);
              } else if (event.type === 'error') {
                onError(event.content || 'Unknown error');
              } else if (event.type === 'done') {
                onDone();
                return;
              }
            } catch {
              // 如果解析失败，忽略
              console.warn('Failed to parse SSE data:', data);
            }
          }
        }
      }
      onDone();
    })
    .catch((err) => {
      if (err.name !== 'AbortError') {
        onError(err.message);
      }
    });

  return () => controller.abort();
}

export default api;
