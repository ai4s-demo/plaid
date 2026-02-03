// 源板数据
export interface SourcePlate {
  plateId: string;
  wells: SourceWell[];
  totalGenes: number;
  totalVolume: number;
}

export interface SourceWell {
  wellId: string;
  geneId: string;
  geneName: string;
  concentration: number;
  volume: number;
}

// 设计参数
export interface DesignParameters {
  plateFormat: 96 | 384 | 1536;
  replicates: number;
  edgeLayers: number;
  distribution: 'uniform' | 'random';
  controlSpread: boolean;
  quadrantBalance: boolean;
  noAdjacent: boolean;
}

// 板布局
export interface PlateLayout {
  layoutId: string;
  plateFormat: 96 | 384 | 1536;
  wells: LayoutWell[];
  violations: ConstraintViolation[];
  score: number;
  createdAt: string;
}

export interface LayoutWell {
  wellId: string;
  row: number;
  col: number;
  geneId: string | null;
  geneName: string | null;
  wellType: 'sample' | 'control' | 'empty' | 'edge';
  replicateIndex: number;
}

export interface ConstraintViolation {
  type: string;
  severity: 'error' | 'warning';
  message: string;
  wells: string[];
}

// Picklist
export interface PicklistEntry {
  sourceBarcode: string;
  sourceWell: string;
  destBarcode: string;
  destWell: string;
  volume: number;
  geneId: string;
  geneName: string;
}

// 聊天消息
export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  attachments?: Attachment[];
  layout?: PlateLayout;  // 关联的布局
}

export interface Attachment {
  type: 'file' | 'layout';
  name: string;
  data: SourcePlate | PlateLayout;
}

// API 请求/响应
export interface ChatRequest {
  message: string;
  context?: ChatContext;
  history?: Array<{ role: string; content: string }>;
}

export interface ChatContext {
  sourcePlate: SourcePlate | null;
  currentLayout: PlateLayout | null;
  parameters: DesignParameters;
}

export interface LayoutRequest {
  sourcePlate: SourcePlate;
  parameters: DesignParameters;
}

export interface UpdateLayoutRequest {
  layout: PlateLayout;
  changes: WellChange[];
}

export interface WellChange {
  wellId: string;
  newGeneId: string | null;
  newWellType?: 'sample' | 'control' | 'empty';
}

// SSE 事件
export interface SSEEvent {
  type: 'message' | 'layout' | 'error' | 'done';
  data: string | PlateLayout | { message: string };
}

// 应用状态
export interface AppState {
  sourcePlate: SourcePlate | null;
  currentLayout: PlateLayout | null;
  parameters: DesignParameters;
  messages: ChatMessage[];
  isLoading: boolean;
  error: string | null;
}

// 默认参数
export const DEFAULT_PARAMETERS: DesignParameters = {
  plateFormat: 96,
  replicates: 6,
  edgeLayers: 1,
  distribution: 'uniform',
  controlSpread: true,
  quadrantBalance: true,
  noAdjacent: true,
};
