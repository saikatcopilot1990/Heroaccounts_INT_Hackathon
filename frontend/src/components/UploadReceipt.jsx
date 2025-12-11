import { useState } from 'react'
import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8800/api/v1'

export default function UploadReceipt({ onUploadSuccess }) {
    const [file, setFile] = useState(null)
    const [uploading, setUploading] = useState(false)

    const handleFileChange = (e) => {
        if (e.target.files) {
            setFile(e.target.files[0])
        }
    }

    const handleUpload = async () => {
        if (!file) return
        setUploading(true)

        const formData = new FormData()
        formData.append('file', file)

        try {
            const res = await axios.post(`${API_BASE}/upload-receipt`, formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            })
            onUploadSuccess(res.data)
            setFile(null)
        } catch (error) {
            console.error("Upload failed", error)
            alert("Upload failed")
        } finally {
            setUploading(false)
        }
    }

    return (
        <div className="card">
            <h2>Upload Receipt</h2>
            <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
                <input type="file" accept=".pdf" onChange={handleFileChange} />
                <button onClick={handleUpload} disabled={!file || uploading}>
                    {uploading ? 'Processing...' : 'Upload & Extract'}
                </button>
            </div>
        </div>
    )
}
