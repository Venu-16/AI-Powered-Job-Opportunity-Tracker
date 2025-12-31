import React, { useState } from 'react'
import axios from 'axios'

export default function ResumeUpload({onUploaded}){
  const [file, setFile] = useState(null)
  const [roles, setRoles] = useState('Backend Developer')
  const [companies, setCompanies] = useState('Amazon,Google')
  const [loading, setLoading] = useState(false)

  const upload = async () => {
    if(!file) return alert('Select a resume file')
    setLoading(true)
    const fd = new FormData()
    fd.append('file', file)
    try{
      const r = await axios.post('/api/resume/upload', fd, { headers: { 'Content-Type': 'multipart/form-data' } })
      const id = r.data.resume_id
      onUploaded(id)
      // call fetch jobs
      const resp = await axios.post('/api/jobs/fetch', { roles: roles.split(','), companies: companies.split(',') })
      alert(`Jobs fetched: ${resp.data.jobs_fetched}`)
    }catch(e){
      console.error(e)
      alert('Upload or fetch failed')
    }finally{
      setLoading(false)
    }
  }

  return (
    <div className="card">
      <h2>Upload Resume</h2>
      <input type="file" onChange={(e)=>setFile(e.target.files[0])} />
      <div>
        <label>Roles (comma separated)</label>
        <input value={roles} onChange={(e)=>setRoles(e.target.value)} />
      </div>
      <div>
        <label>Companies (comma separated)</label>
        <input value={companies} onChange={(e)=>setCompanies(e.target.value)} />
      </div>
      <button onClick={upload} disabled={loading}>{loading ? 'Working...' : 'Upload & Fetch Jobs'}</button>
    </div>
  )
}
