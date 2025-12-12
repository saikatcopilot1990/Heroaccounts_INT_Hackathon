import { useState, useEffect } from 'react'
import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8800/api/v1'

// Helper to map array of extracted fields into nice key-value pairs for the form
const mapExtractedDataToForm = (dataArr) => {
    if (!Array.isArray(dataArr)) return {}
    const map = {};
    dataArr.forEach(item => {
            map[item.label] = item.value ?? '';
    });
    return map;
};

export default function ClaimDetails({ receiptData, onBack, onSubmitSuccess }) {
    const [formData, setFormData] = useState({
        amount: '',
        date: '',
        vendor: '',
        category: '',
        gst: '',
        description: '',
        employee_id: 1,
        receipt_id: undefined
    })

    const [validation, setValidation] = useState(null)
    const [budget, setBudget] = useState(null)
    const [submitting, setSubmitting] = useState(false)

    useEffect(() => {
        if (receiptData && Array.isArray(receiptData.extracted_data)) {
            const mapped = mapExtractedDataToForm(receiptData.extracted_data)
            setFormData(prev => ({
                ...prev,
                ...mapped,
                receipt_id: receiptData.receipt_id
            }))
        }
    }, [receiptData])

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value })
    }

    const handleSubmit = async () => {
        setSubmitting(true)
        try {
            const submission = {
                ...formData,
                receipt_id: receiptData?.receipt_id ?? formData.receipt_id,
                employee_id: formData.employee_id
            }
            const res = await axios.post(`${API_BASE}/submit-claim`, submission)
            alert("Claim Submitted Successfully!")
            onSubmitSuccess()
        } catch (error) {
            console.error("Submit failed", error)
            alert(`Submit Failed: ${error.response?.data?.detail || error.message}`)
        } finally {
            setSubmitting(false)
        }
    }

    return (
        <div className="card">
            {console.log(formData,'DDDDDD')}
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <h2>Claim Details</h2>
                <button onClick={onBack}>Back</button>
            </div>

            <div className="grid-form">
                <label>Amount</label>
                <input
                    name="amount"
                    value={formData.amount || ''}
                    onChange={handleChange}
                />

                <label>Date</label>
                <input
                    name="date"
                    value={formData.date || ''}
                    onChange={handleChange}
                    placeholder="YYYY-MM-DD"
                />

                <label>Vendor</label>
                <input
                    name="vendor"
                    value={formData.vendor || ''}
                    onChange={handleChange}
                />

                <label>Category</label>
                <select
                    name="category"
                    value={formData.category || ''}
                    onChange={handleChange}
                >
                    <option value="">Select...</option>
                    <option value="Travel">Travel</option>
                    <option value="Food">Food</option>
                    <option value="Hotel">Hotel</option>
                    <option value="Others">Others</option>
                </select>

                <label>GST No</label>
                <input
                    name="gst"
                    value={formData.gst || ''}
                    onChange={handleChange}
                />
                <label>Description</label>
                <input
                    name="description"
                    value={formData.description || ''}
                    onChange={handleChange}
                />
            </div>

            <div style={{ marginTop: '1rem', display: 'flex', gap: '1rem' }}>
                <button onClick={handleSubmit} disabled={submitting} className="primary">
                    {submitting ? 'Submitting...' : 'Submit Claim'}
                </button>
            </div>
        </div>
    )
}
