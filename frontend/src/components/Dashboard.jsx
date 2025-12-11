import { useState, useEffect } from 'react'
import axios from 'axios'
import ApproverAction from './ApproverAction'

const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8800/api/v1'

export default function Dashboard({ refreshTrigger }) {
    const [claims, setClaims] = useState([])
    const [loading, setLoading] = useState(false)
    const [selectedClaim, setSelectedClaim] = useState(null)
    const [approverId, setApproverId] = useState(2) // Default to Manager (ID: 2)

    const fetchClaims = async () => {
        setLoading(true)
        try {
            const { data } = await axios.get(`${API_BASE}/claims`)
            setClaims(data)
        } catch (error) {
            console.error('Failed to fetch claims', error)
            alert('Failed to load claims')
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        fetchClaims()
    }, [refreshTrigger])

    const handleClaimClick = (claim) => {
        setSelectedClaim(claim)
    }

    const handleApprovalSuccess = () => {
        setSelectedClaim(null)
        fetchClaims() // Refresh the list
    }

    const handleCloseDetails = () => {
        setSelectedClaim(null)
    }

    return (
        <div className="card">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <h2>Claims Dashboard</h2>
                <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
                    <label>Approver ID:</label>
                    <input
                        type="number"
                        value={approverId}
                        onChange={(e) => setApproverId(parseInt(e.target.value))}
                        style={{ width: '60px', padding: '0.5rem' }}
                    />
                    <span style={{ fontSize: '0.9rem', color: '#6b7280' }}>
                        (1=Finance, 2=Manager, 3=Employee)
                    </span>
                </div>
            </div>

            {loading ? (
                <p>Loading claims...</p>
            ) : (
                <>
                    {selectedClaim && (
                        <div style={{
                            marginTop: '1rem',
                            padding: '1.5rem',
                            border: '2px solid #2563eb',
                            borderRadius: '8px',
                            backgroundColor: '#f0f9ff'
                        }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                <h3>Claim #{selectedClaim.id} - Details</h3>
                                <button onClick={handleCloseDetails}>Close</button>
                            </div>

                            <div style={{ marginTop: '1rem', display: 'grid', gridTemplateColumns: '150px 1fr', gap: '0.5rem' }}>
                                <strong>Employee:</strong> <span>{selectedClaim.employee}</span>
                                <strong>Amount:</strong> <span>₹{selectedClaim.amount}</span>
                                <strong>Date:</strong> <span>{selectedClaim.date}</span>
                                <strong>Vendor:</strong> <span>{selectedClaim.vendor || 'N/A'}</span>
                                <strong>Category:</strong> <span>{selectedClaim.category}</span>
                                <strong>Status:</strong>
                                <span className={`status-badge status-${selectedClaim.status}`}>
                                    {selectedClaim.status.replace(/_/g, ' ')}
                                </span>
                            </div>

                            {selectedClaim.status === 'submitted' || selectedClaim.status === 'approved_by_manager' ? (
                                <ApproverAction
                                    claimId={selectedClaim.id}
                                    approverId={approverId}
                                    onActionSuccess={handleApprovalSuccess}
                                />
                            ) : (
                                <p style={{ marginTop: '1rem', color: '#6b7280' }}>
                                    This claim cannot be approved in its current status.
                                </p>
                            )}
                        </div>
                    )}

                    <div className="table-container" style={{ marginTop: '1rem' }}>
                        <table>
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Employee</th>
                                    <th>Amount</th>
                                    <th>Category</th>
                                    <th>Date</th>
                                    <th>Vendor</th>
                                    <th>Status</th>
                                    <th>Submitted</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {claims.length === 0 ? (
                                    <tr>
                                        <td colSpan="9" style={{ textAlign: 'center' }}>
                                            No claims yet. Upload a receipt to get started.
                                        </td>
                                    </tr>
                                ) : (
                                    claims.map(claim => (
                                        <tr key={claim.id} style={{ cursor: 'pointer' }}>
                                            <td>{claim.id}</td>
                                            <td>{claim.employee}</td>
                                            <td>₹{claim.amount}</td>
                                            <td>{claim.category}</td>
                                            <td>{claim.date}</td>
                                            <td>{claim.vendor || 'N/A'}</td>
                                            <td>
                                                <span className={`status-badge status-${claim.status}`}>
                                                    {claim.status.replace(/_/g, ' ')}
                                                </span>
                                            </td>
                                            <td>{claim.created_at}</td>
                                            <td>
                                                <button
                                                    onClick={() => handleClaimClick(claim)}
                                                    style={{ padding: '0.5rem 1rem', fontSize: '0.875rem' }}
                                                >
                                                    View/Approve
                                                </button>
                                            </td>
                                        </tr>
                                    ))
                                )}
                            </tbody>
                        </table>
                    </div>
                </>
            )}
        </div>
    )
}
