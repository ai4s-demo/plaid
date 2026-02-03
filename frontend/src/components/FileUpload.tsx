import { useCallback, useState } from 'react';
import type { SourcePlate } from '../types';

interface FileUploadProps {
  sourcePlate: SourcePlate | null;
  isLoading: boolean;
  onUpload: (file: File) => Promise<SourcePlate>;
}

export function FileUpload({ sourcePlate, isLoading, onUpload }: FileUploadProps) {
  const [dragActive, setDragActive] = useState(false);

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback(
    async (e: React.DragEvent) => {
      e.preventDefault();
      e.stopPropagation();
      setDragActive(false);

      const file = e.dataTransfer.files[0];
      if (file && (file.name.endsWith('.xlsx') || file.name.endsWith('.csv'))) {
        await onUpload(file);
      }
    },
    [onUpload]
  );

  const handleChange = useCallback(
    async (e: React.ChangeEvent<HTMLInputElement>) => {
      const file = e.target.files?.[0];
      if (file) {
        await onUpload(file);
      }
    },
    [onUpload]
  );

  return (
    <div className="file-upload">
      <h3>📁 源板文件</h3>

      {!sourcePlate ? (
        <div
          className={`upload-zone ${dragActive ? 'active' : ''}`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <input
            type="file"
            accept=".xlsx,.csv"
            onChange={handleChange}
            disabled={isLoading}
            id="file-input"
            className="file-input"
          />
          <label htmlFor="file-input" className="upload-label">
            {isLoading ? (
              <span>解析中...</span>
            ) : (
              <>
                <span className="upload-icon">📤</span>
                <span>拖拽文件到这里或点击上传</span>
                <span className="upload-hint">支持 .xlsx, .csv</span>
              </>
            )}
          </label>
        </div>
      ) : (
        <div className="source-info">
          <div className="info-item">
            <span className="label">板 ID:</span>
            <span className="value">{sourcePlate.plateId}</span>
          </div>
          <div className="info-item">
            <span className="label">基因数:</span>
            <span className="value">{sourcePlate.totalGenes}</span>
          </div>
          <div className="info-item">
            <span className="label">孔位数:</span>
            <span className="value">{sourcePlate.wells.length}</span>
          </div>
          <button
            className="btn btn-secondary"
            onClick={() => window.location.reload()}
          >
            重新上传
          </button>
        </div>
      )}
    </div>
  );
}
