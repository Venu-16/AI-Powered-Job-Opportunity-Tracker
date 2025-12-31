import React, { useState } from 'react'
import ResumeUpload from './components/ResumeUpload'
import JobResults from './components/JobResults'

export default function App(){
  const [resumeId, setResumeId] = useState(null)
  return (
    <div className="container">
      <h1>Job Matcher</h1>
      <ResumeUpload onUploaded={(id) => setResumeId(id)} />
      {resumeId && <JobResults resumeId={resumeId} />}
    </div>
  )
}
