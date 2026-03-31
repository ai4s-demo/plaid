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

  // Download Picklist CSV
  const downloadPicklist = useCallback(async () => {
    if (!layout || !sourcePlate) return;
    setIsGenerating(true);

    try {
      const picklist = await generatePicklist(layout, sourcePlate);
      const csv = generateCSV(picklist);
      downloadFile(csv, `picklist_${layout.layoutId}.csv`, 'text/csv');
    } catch (err) {
      console.error('Failed to generate Picklist:', err);
    } finally {
      setIsGenerating(false);
    }
  }, [layout, sourcePlate]);

  // Download layout JSON
  const downloadJSON = useCallback(() => {
    if (!layout) return;
    const json = JSON.stringify(layout, null, 2);
    downloadFile(json, `layout_${layout.layoutId}.json`, 'application/json');
  }, [layout]);

  // Download PDF report
  const downloadPDF = useCallback(() => {
    if (!layout) return;
    setIsGenerating(true);

    try {
      const doc = new jsPDF();
      const { plateFormat, wells, score, violations, layoutId, createdAt } = layout;

      // Title
      doc.setFontSize(18);
      doc.text('Smart Campaign Designer - Layout Report', 20, 20);

      // Basic info
      doc.setFontSize(12);
      doc.text(`Layout ID: ${layoutId}`, 20, 35);
      doc.text(`Plate Format: ${plateFormat}-Well`, 20, 45);
      doc.text(`Optimization Score: ${score.toFixed(2)}`, 20, 55);
      doc.text(`Generated: ${new Date(createdAt).toLocaleString()}`, 20, 65);

      // Statistics
      const sampleCount = wells.filter((w) => w.wellType === 'sample').length;
      const controlCount = wells.filter((w) => w.wellType === 'control').length;
      const emptyCount = wells.filter((w) => w.wellType === 'empty').length;
      const edgeCount = wells.filter((w) => w.wellType === 'edge').length;

      doc.text('Well Statistics:', 20, 80);
      doc.text(`  Samples: ${sampleCount}`, 25, 90);
      doc.text(`  Controls: ${controlCount}`, 25, 100);
      doc.text(`  Empty: ${emptyCount}`, 25, 110);
      doc.text(`  Edge: ${edgeCount}`, 25, 120);

      // Violations
      if (violations.length > 0) {
        doc.text('Constraint Violations:', 20, 135);
        violations.forEach((v, i) => {
          doc.text(`  ${i + 1}. ${v.message}`, 25, 145 + i * 10);
        });
      }

      // Draw plate layout
      const rows = plateFormat === 96 ? 8 : 16;
      const cols = plateFormat === 96 ? 12 : 24;
      const cellSize = plateFormat === 96 ? 12 : 6;
      const startX = 20;
      const startY = violations.length > 0 ? 170 : 140;

      // Row labels
      for (let r = 0; r < rows; r++) {
        doc.setFontSize(8);
        doc.text(String.fromCharCode(65 + r), startX - 8, startY + r * cellSize + cellSize / 2 + 2);
      }

      // Column labels
      for (let c = 0; c < cols; c++) {
        doc.text(String(c + 1), startX + c * cellSize + cellSize / 2 - 2, startY - 3);
      }

      // Wells
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
        <h3>📥 Download</h3>
        <p className="hint">Available after layout generation</p>
      </div>
    );
  }

  const canDownloadPicklist = layout && sourcePlate;

  return (
    <div className="download-panel">
      <h3>📥 Download</h3>
      <div className="download-buttons">
        <button
          className="btn btn-download"
          onClick={downloadPicklist}
          disabled={isGenerating || !canDownloadPicklist}
          title={!canDownloadPicklist ? 'Source plate data required to generate Picklist' : ''}
        >
          📋 Picklist (CSV)
        </button>
        <button
          className="btn btn-download"
          onClick={downloadJSON}
          disabled={isGenerating}
        >
          📄 Layout (JSON)
        </button>
        <button
          className="btn btn-download"
          onClick={downloadPDF}
          disabled={isGenerating}
        >
          📑 Report (PDF)
        </button>
      </div>
    </div>
  );
}

// Helper functions
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
