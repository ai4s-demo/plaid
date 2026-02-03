import { useState, useCallback } from 'react';
import { jsPDF } from 'jspdf';
import type { PlateLayout, PicklistEntry, SourcePlate } from '../types';
import { generatePicklist } from '../services/api';

interface DownloadPanelProps {
  layout: PlateLayout | null;
  sourcePlate: SourcePlate | null;
}

export function DownloadPanel({ layout, sourcePlate }: DownloadPanelProps) {
  const [isGenerating, setIsGenerating] = useState(false);

  // 下载 Picklist CSV
  const downloadPicklist = useCallback(async () => {
    if (!layout || !sourcePlate) return;
    setIsGenerating(true);

    try {
      const picklist = await generatePicklist(layout, sourcePlate);
      const csv = generateCSV(picklist);
      downloadFile(csv, `picklist_${layout.layoutId}.csv`, 'text/csv');
    } catch (err) {
      console.error('生成 Picklist 失败:', err);
    } finally {
      setIsGenerating(false);
    }
  }, [layout, sourcePlate]);

  // 下载布局 JSON
  const downloadJSON = useCallback(() => {
    if (!layout) return;
    const json = JSON.stringify(layout, null, 2);
    downloadFile(json, `layout_${layout.layoutId}.json`, 'application/json');
  }, [layout]);

  // 下载 PDF 报告
  const downloadPDF = useCallback(() => {
    if (!layout) return;
    setIsGenerating(true);

    try {
      const doc = new jsPDF();
      const { plateFormat, wells, score, violations, layoutId, createdAt } = layout;

      // 标题
      doc.setFontSize(18);
      doc.text('Smart Campaign Designer - 布局报告', 20, 20);

      // 基本信息
      doc.setFontSize(12);
      doc.text(`布局 ID: ${layoutId}`, 20, 35);
      doc.text(`板格式: ${plateFormat} 孔`, 20, 45);
      doc.text(`优化得分: ${score.toFixed(2)}`, 20, 55);
      doc.text(`生成时间: ${new Date(createdAt).toLocaleString()}`, 20, 65);

      // 统计
      const sampleCount = wells.filter((w) => w.wellType === 'sample').length;
      const controlCount = wells.filter((w) => w.wellType === 'control').length;
      const emptyCount = wells.filter((w) => w.wellType === 'empty').length;
      const edgeCount = wells.filter((w) => w.wellType === 'edge').length;

      doc.text('孔位统计:', 20, 80);
      doc.text(`  样本: ${sampleCount}`, 25, 90);
      doc.text(`  对照: ${controlCount}`, 25, 100);
      doc.text(`  空孔: ${emptyCount}`, 25, 110);
      doc.text(`  边缘: ${edgeCount}`, 25, 120);

      // 违规
      if (violations.length > 0) {
        doc.text('约束违规:', 20, 135);
        violations.forEach((v, i) => {
          doc.text(`  ${i + 1}. ${v.message}`, 25, 145 + i * 10);
        });
      }

      // 绘制板布局
      const rows = plateFormat === 96 ? 8 : 16;
      const cols = plateFormat === 96 ? 12 : 24;
      const cellSize = plateFormat === 96 ? 12 : 6;
      const startX = 20;
      const startY = violations.length > 0 ? 170 : 140;

      // 行标签
      for (let r = 0; r < rows; r++) {
        doc.setFontSize(8);
        doc.text(String.fromCharCode(65 + r), startX - 8, startY + r * cellSize + cellSize / 2 + 2);
      }

      // 列标签
      for (let c = 0; c < cols; c++) {
        doc.text(String(c + 1), startX + c * cellSize + cellSize / 2 - 2, startY - 3);
      }

      // 孔位
      wells.forEach((well) => {
        const x = startX + well.col * cellSize;
        const y = startY + well.row * cellSize;

        let color: [number, number, number] = [245, 245, 245];
        if (well.wellType === 'edge') color = [224, 224, 224];
        else if (well.wellType === 'control') color = [76, 175, 80];
        else if (well.wellType === 'sample') color = [33, 150, 243];

        doc.setFillColor(...color);
        doc.rect(x, y, cellSize - 1, cellSize - 1, 'F');
      });

      doc.save(`layout_report_${layoutId}.pdf`);
    } finally {
      setIsGenerating(false);
    }
  }, [layout]);

  if (!layout) {
    return (
      <div className="download-panel disabled">
        <h3>📥 下载</h3>
        <p className="hint">生成布局后可下载</p>
      </div>
    );
  }

  const canDownloadPicklist = layout && sourcePlate;

  return (
    <div className="download-panel">
      <h3>📥 下载</h3>
      <div className="download-buttons">
        <button
          className="btn btn-download"
          onClick={downloadPicklist}
          disabled={isGenerating || !canDownloadPicklist}
          title={!canDownloadPicklist ? '需要源板数据才能生成Picklist' : ''}
        >
          📋 Picklist (CSV)
        </button>
        <button
          className="btn btn-download"
          onClick={downloadJSON}
          disabled={isGenerating}
        >
          📄 布局 (JSON)
        </button>
        <button
          className="btn btn-download"
          onClick={downloadPDF}
          disabled={isGenerating}
        >
          📑 报告 (PDF)
        </button>
      </div>
    </div>
  );
}

// 辅助函数
function generateCSV(picklist: PicklistEntry[]): string {
  const headers = [
    'Source Barcode',
    'Source Well',
    'Dest Barcode',
    'Dest Well',
    'Volume',
    'Gene ID',
    'Gene Name',
  ];
  const rows = picklist.map((p) => [
    p.sourceBarcode,
    p.sourceWell,
    p.destBarcode,
    p.destWell,
    String(p.volume),
    p.geneId,
    p.geneName,
  ]);
  return [headers, ...rows].map((r) => r.join(',')).join('\n');
}

function downloadFile(content: string, filename: string, type: string) {
  const blob = new Blob([content], { type });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}
