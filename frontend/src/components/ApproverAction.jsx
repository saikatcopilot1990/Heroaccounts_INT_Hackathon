import { useState } from 'react'
import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8800/api/v1'

export default function ApproverAction({ claimId, approverId, onActionSuccess }) {
    const [comments, setComments] = useState('')
    const [processing, setProcessing] = useState(false)

    const handleAction = async (action) => {
        setProcessing(true)
        try {
            await axios.post(`${API_BASE}/approve-claim`, {
                claim_id: claimId,
                approver_id: approverId,
                action: action,
                comments: comments
            })
            alert(`Claim ${action}ed successfully`)
            onActionSuccess()
        } catch (error) {
            console.error("Action failed", error)
            alert(`Action Failed: ${error.response?.data?.detail || error.message}`)
        } finally {
            setProcessing(false)
        }
    }

    return (
        <div style={{ marginTop: '1rem', borderTop: '1px solid #eee', paddingTop: '1rem' }}>
            <h4>Approver Actions</h4>
            <textarea
                placeholder="Comments (optional)"
                value={comments}
                onChange={(e) => setComments(e.target.value)}
                style={{ width: '100%', marginBottom: '0.5rem' }}
            />
            <div style={{ display: 'flex', gap: '1rem' }}>
                <button
                    onClick={() => handleAction('approve')}
                    disabled={processing}
                    style={{ backgroundColor: '#4CAF50', color: 'white' }}
                >
                    Approve
                </button>
                <button
                    onClick={() => handleAction('reject')}
                    disabled={processing}
                    style={{ backgroundColor: '#f44336', color: 'white' }}
                >
                    Reject
                </button>
            </div>
        </div>
    )
}
