import React, { useEffect, useState } from 'react'
import axios from 'axios'

export default function JobResults({resumeId}){
  const [jobs, setJobs] = useState([])
  useEffect(()=>{
    const load = async ()=>{
      try{
        const r = await axios.get(`/api/match/results/${resumeId}`)
        setJobs(r.data)
      }catch(e){
        console.error(e)
      }
    }
    load()
  }, [resumeId])

  return (
    <div className="card">
      <h2>Job Matches</h2>
      {jobs.length === 0 && <div>No matches yet</div>}
      {jobs.map((j, idx)=> (
        <div key={idx} className="job">
          <h3>{j.title} <small>— {j.company}</small></h3>
          <div>Match: {j.score}%</div>
          <div>Missing: {j.missing_skills.join(', ')}</div>
          <div><a href={j.apply_url} target="_blank" rel="noreferrer">Apply</a></div>
        </div>
      ))}
    </div>
  )
}
