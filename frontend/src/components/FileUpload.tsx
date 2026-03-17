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
      <h3>📁 Source Plate File</h3>

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
              <span>Parsing...</span>
            ) : (
              <>
                <span className="upload-icon">📤</span>
                <span>Drag file here or click to upload</span>
                <span className="upload-hint">Supports .xlsx, .csv</span>
              </>
            )}
          </label>
        </div>
      ) : (
        <div className="source-info">
          <div className="info-item">
            <span className="label">Plate ID:</span>
            <span className="value">{sourcePlate.plateId}</span>
          </div>
          <div className="info-item">
            <span className="label">Genes:</span>
            <span className="value">{sourcePlate.totalGenes}</span>
          </div>
          <div className="info-item">
            <span className="label">Wells:</span>
            <span className="value">{sourcePlate.wells.length}</span>
          </div>
          <button
            className="btn btn-secondary"
            onClick={() => window.location.reload()}
          >
            Re-upload
          </button>
        </div>
      )}
    </div>
  );
}
