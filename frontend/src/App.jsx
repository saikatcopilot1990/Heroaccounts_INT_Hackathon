import { useState } from 'react'
import UploadReceipt from './components/UploadReceipt'
import ClaimDetails from './components/ClaimDetails'
import Dashboard from './components/Dashboard'
import ApproverAction from './components/ApproverAction'

function App() {
  const [view, setView] = useState('upload') // upload, claim-details, dashboard
  const [receiptData, setReceiptData] = useState(null)
  const [refreshTrigger, setRefreshTrigger] = useState(0)

  const handleUploadSuccess = (data) => {
    setReceiptData(data)
    setView('claim-details')
  }

  const handleSubmitSuccess = () => {
    setRefreshTrigger(prev => prev + 1)
    setView('dashboard')
  }

  const handleBack = () => {
    setView('upload')
  }

  return (
    <div className="app-shell">
      <header className="app-header">
        <h1>HeroAccounts Reimbursement Automation</h1>
        <p>Upload receipts, auto-validate, and streamline approvals.</p>
      </header>

      <nav className="app-nav">
        <button
          className={view === 'upload' ? 'active' : ''}
          onClick={() => setView('upload')}
        >
          Upload Receipt
        </button>
        <button
          className={view === 'dashboard' ? 'active' : ''}
          onClick={() => setView('dashboard')}
        >
          Dashboard
        </button>
      </nav>

      <div className="workspace">
        {view === 'upload' && (
          <UploadReceipt onUploadSuccess={handleUploadSuccess} />
        )}

        {view === 'claim-details' && receiptData && (
          <ClaimDetails
            receiptData={receiptData}
            onBack={handleBack}
            onSubmitSuccess={handleSubmitSuccess}
          />
        )}

        {view === 'dashboard' && (
          <Dashboard refreshTrigger={refreshTrigger} />
        )}
      </div>
    </div>
  )
}

export default App
