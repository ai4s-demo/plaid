import { useMemo, useState, useCallback } from 'react';
import {
  DndContext,
  DragEndEvent,
  DragStartEvent,
  DragOverlay,
  useDraggable,
  useDroppable,
} from '@dnd-kit/core';
import type { PlateLayout, LayoutWell } from '../types';

interface PlateViewProps {
  layout: PlateLayout | null;
  onLayoutChange: (layout: PlateLayout) => void;
  compact?: boolean;  // 紧凑模式，用于聊天内嵌显示
}

// 颜色映射
const WELL_COLORS: Record<string, string> = {
  empty: '#f5f5f5',
  edge: '#e0e0e0',
  control: '#4caf50',
  positive_control: '#4caf50',
  negative_control: '#f44336',
  blank: '#9e9e9e',
  sample: '#2196f3',
};

// 预定义高区分度颜色调色板
const GENE_PALETTE = [
  '#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231',
  '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe',
  '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000',
  '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080',
  '#ff6f61', '#6b5b95', '#88b04b', '#f7cac9', '#92a8d1',
  '#955251', '#b565a7', '#009b77', '#dd4124', '#45b8ac',
];

// 基因颜色生成 - 使用预定义调色板确保高区分度
function getGeneColor(geneId: string, allGeneIds: string[]): string {
  // 按字母排序后找到索引，确保稳定性
  const sortedGenes = [...allGeneIds].sort((a, b) => {
    // 自然排序：Gene1, Gene2, ..., Gene10, Gene11
    const numA = parseInt(a.replace(/\D/g, '')) || 0;
    const numB = parseInt(b.replace(/\D/g, '')) || 0;
    if (numA !== numB) return numA - numB;
    return a.localeCompare(b);
  });
  const index = sortedGenes.indexOf(geneId);
  if (index === -1) return '#2196f3';
  return GENE_PALETTE[index % GENE_PALETTE.length];
}

// 单个孔位组件
function Well({
  well,
  allGeneIds,
  isDragging,
  cellSize,
  wellRadius,
  fontSize,
  labelOffset,
}: {
  well: LayoutWell;
  allGeneIds: string[];
  isDragging: boolean;
  cellSize: number;
  wellRadius: number;
  fontSize: number;
  labelOffset: number;
}) {
  const { attributes, listeners, setNodeRef, transform } = useDraggable({
    id: well.wellId,
    data: well,
    disabled: well.wellType === 'empty' || well.wellType === 'edge',
  });

  const { setNodeRef: setDropRef, isOver } = useDroppable({
    id: `drop-${well.wellId}`,
    data: well,
  });

  const color = useMemo(() => {
    // 样本类型且有基因ID时，使用基因特定颜色
    if (well.wellType === 'sample' && well.geneId) {
      return getGeneColor(well.geneId, allGeneIds);
    }
    // 其他类型使用预定义颜色
    return WELL_COLORS[well.wellType] || WELL_COLORS.empty;
  }, [well.wellType, well.geneId, allGeneIds]);

  const style = {
    transform: transform
      ? `translate(${transform.x}px, ${transform.y}px)`
      : undefined,
    opacity: isDragging ? 0.5 : 1,
  };

  const cx = well.col * cellSize + labelOffset + 10;
  const cy = well.row * cellSize + labelOffset + 10;

  return (
    <g
      ref={(node) => {
        setNodeRef(node as unknown as HTMLElement);
        setDropRef(node as unknown as HTMLElement);
      }}
      {...attributes}
      {...listeners}
      style={{ cursor: well.wellType === 'sample' ? 'grab' : 'default' }}
    >
      <circle
        cx={cx}
        cy={cy}
        r={wellRadius}
        fill={color}
        stroke={isOver ? '#ff9800' : '#999'}
        strokeWidth={isOver ? 2 : 1}
        style={style}
      />
      {well.geneId && fontSize >= 6 && (
        <text
          x={cx}
          y={cy + fontSize / 3}
          textAnchor="middle"
          fontSize={fontSize}
          fill="#fff"
          pointerEvents="none"
        >
          {well.geneName?.slice(0, 4) || well.geneId.slice(0, 4)}
        </text>
      )}
    </g>
  );
}

export function PlateView({ layout, onLayoutChange, compact = false }: PlateViewProps) {
  const [activeId, setActiveId] = useState<string | null>(null);

  const { rows, cols, geneIds } = useMemo(() => {
    if (!layout) return { rows: 8, cols: 12, geneIds: [] };
    // 根据板类型设置行列数
    let r = 8, c = 12;  // 96孔板默认
    if (layout.plateFormat === 384) {
      r = 16; c = 24;
    } else if (layout.plateFormat === 1536) {
      r = 32; c = 48;
    }
    // 获取唯一基因并使用自然排序
    const ids = [...new Set(layout.wells.filter((w) => w.geneId).map((w) => w.geneId!))];
    ids.sort((a, b) => {
      const numA = parseInt(a.replace(/\D/g, '')) || 0;
      const numB = parseInt(b.replace(/\D/g, '')) || 0;
      if (numA !== numB) return numA - numB;
      return a.localeCompare(b);
    });
    return { rows: r, cols: c, geneIds: ids };
  }, [layout]);

  const handleDragStart = useCallback((event: DragStartEvent) => {
    setActiveId(event.active.id as string);
  }, []);

  const handleDragEnd = useCallback(
    (event: DragEndEvent) => {
      setActiveId(null);
      if (!layout || !event.over) return;

      const sourceWellId = event.active.id as string;
      const targetWellId = (event.over.id as string).replace('drop-', '');

      if (sourceWellId === targetWellId) return;

      const sourceWell = layout.wells.find((w) => w.wellId === sourceWellId);
      const targetWell = layout.wells.find((w) => w.wellId === targetWellId);

      if (!sourceWell || !targetWell) return;
      if (targetWell.wellType === 'edge') return;

      // 交换两个孔位的内容
      const newWells = layout.wells.map((w) => {
        if (w.wellId === sourceWellId) {
          // 源孔获得目标孔的内容
          return {
            ...w,
            geneId: targetWell.geneId,
            geneName: targetWell.geneName,
            wellType: targetWell.geneId ? 'sample' : 'empty',
            replicateIndex: targetWell.replicateIndex,
          } as LayoutWell;
        }
        if (w.wellId === targetWellId) {
          // 目标孔获得源孔的内容
          return {
            ...w,
            geneId: sourceWell.geneId,
            geneName: sourceWell.geneName,
            wellType: sourceWell.geneId ? 'sample' : 'empty',
            replicateIndex: sourceWell.replicateIndex,
          } as LayoutWell;
        }
        return w;
      });

      onLayoutChange({ ...layout, wells: newWells });
    },
    [layout, onLayoutChange]
  );

  if (!layout) {
    return (
      <div className="plate-view empty">
        <div className="plate-placeholder">
          <span>🧫</span>
          <p>布局将在这里显示</p>
        </div>
      </div>
    );
  }

  // 紧凑模式使用更小的尺寸
  const sizeMultiplier = compact ? 0.5 : 1;
  
  // 根据板类型调整间距
  const baseCellSize = layout.plateFormat === 384 ? 28 : layout.plateFormat === 1536 ? 14 : 40;
  const baseWellRadius = layout.plateFormat === 384 ? 11 : layout.plateFormat === 1536 ? 5 : 16;
  const baseFontSize = layout.plateFormat === 384 ? 6 : layout.plateFormat === 1536 ? 4 : 8;
  const baseLabelOffset = layout.plateFormat === 384 ? 20 : layout.plateFormat === 1536 ? 10 : 30;
  
  const cellSize = baseCellSize * sizeMultiplier;
  const wellRadius = baseWellRadius * sizeMultiplier;
  const fontSize = compact ? 0 : baseFontSize;  // 紧凑模式不显示文字
  const labelOffset = baseLabelOffset * sizeMultiplier;
  
  const width = cols * cellSize + labelOffset * 2 + 20;
  const height = rows * cellSize + labelOffset * 2 + 20;
  const labelFontSize = (layout.plateFormat === 384 ? 9 : layout.plateFormat === 1536 ? 6 : 12) * sizeMultiplier;

  return (
    <div className={`plate-view ${compact ? 'compact' : ''}`}>
      {!compact && (
        <div className="plate-header">
          <h3>🧫 板布局</h3>
          <span className="plate-info">
            {layout.plateFormat}孔板 | 得分: {layout.score.toFixed(2)}
          </span>
        </div>
      )}

      <DndContext onDragStart={handleDragStart} onDragEnd={handleDragEnd}>
        <svg width={width} height={height} className="plate-svg">
          {/* 行标签 */}
          {!compact && Array.from({ length: rows }, (_, i) => (
            <text 
              key={`row-${i}`} 
              x={labelOffset / 2} 
              y={i * cellSize + labelOffset + 10 + labelFontSize / 3} 
              textAnchor="middle" 
              fontSize={labelFontSize}
            >
              {String.fromCharCode(65 + i)}
            </text>
          ))}

          {/* 列标签 */}
          {!compact && Array.from({ length: cols }, (_, i) => (
            <text 
              key={`col-${i}`} 
              x={i * cellSize + labelOffset + 10} 
              y={labelOffset / 2 + labelFontSize / 3} 
              textAnchor="middle" 
              fontSize={labelFontSize}
            >
              {String(i + 1).padStart(2, '0')}
            </text>
          ))}

          {/* 孔位 */}
          {layout.wells.map((well) => (
            <Well
              key={well.wellId}
              well={well}
              allGeneIds={geneIds}
              isDragging={activeId === well.wellId}
              cellSize={cellSize}
              wellRadius={wellRadius}
              fontSize={fontSize}
              labelOffset={compact ? 5 : labelOffset}
            />
          ))}
        </svg>

        {!compact && (
          <DragOverlay>
            {activeId && (
              <div className="drag-overlay">
                {layout.wells.find((w) => w.wellId === activeId)?.geneName || activeId}
              </div>
            )}
          </DragOverlay>
        )}
      </DndContext>

      {/* 图例 - 紧凑模式不显示 */}
      {!compact && (
        <div className="plate-legend">
          <div className="legend-section">
            <div className="legend-item">
              <span className="legend-color" style={{ background: WELL_COLORS.empty }}></span>
              <span>空/边缘</span>
            </div>
            <div className="legend-item">
              <span className="legend-color" style={{ background: WELL_COLORS.positive_control }}></span>
              <span>阳性对照</span>
            </div>
            <div className="legend-item">
              <span className="legend-color" style={{ background: WELL_COLORS.negative_control }}></span>
              <span>阴性对照</span>
            </div>
          </div>
          {geneIds.length > 0 && (
            <div className="legend-section gene-legend">
              <span className="legend-title">基因:</span>
              {geneIds.slice(0, 12).map((geneId) => (
                <div key={geneId} className="legend-item">
                  <span className="legend-color" style={{ background: getGeneColor(geneId, geneIds) }}></span>
                  <span>{geneId.slice(0, 8)}</span>
                </div>
              ))}
              {geneIds.length > 12 && <span className="legend-more">+{geneIds.length - 12} 更多</span>}
            </div>
          )}
        </div>
      )}

      {/* 违规警告 - 紧凑模式不显示 */}
      {!compact && layout.violations.length > 0 && (
        <div className="violations">
          <h4>⚠️ 约束违规</h4>
          {layout.violations.map((v, i) => (
            <div key={i} className={`violation ${v.severity}`}>
              {v.message}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
