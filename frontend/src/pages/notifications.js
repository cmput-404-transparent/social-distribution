import { useEffect, useState } from "react"

function FollowRequest({request}) {
  return(
    <div className="border rounded">
      <div className="grid grid-cols-[min-content,auto] auto-cols-auto border-b p-5">
          <div className="pr-8">
            profile picture
          </div>
          <div className="grid grid-flow-row auto-rows-auto space-y-4">
            <div className="grid grid-cols-[auto,auto]">
              <div>
                <h1 className="font-bold text-l">{request.display_name}</h1>
                <h2 className="text-l">@{request.username}</h2>
              </div>
              <div className="space-x-2 flex justify-end">
                <button type="submit" className='bg-sky-400 rounded p-2 px-4'>Accept</button>
                <button type="submit" className='bg-neutral-200 rounded p-2 px-4'>Delete</button>
              </div>
            </div>
          </div>
        </div>
    </div>
  )
}

export default function Notifications() {
  const [followRequests, setFollowRequests] = useState([]);

  const authorId = localStorage.getItem('authorId');

  useEffect(() => {
    fetch(`/api/authors/${authorId}/follow_requests/`)
    .then((response) => response.json())
    .then((data) => setFollowRequests(data));
  }, [])

  return (
    <div className="page">
      <div className="w-5/6 justify-center flex">
        <div className="grid grid-flow-row auto-rows-auto w-3/4">
          <div className="grid grid-rows-[min-content,auto] space-y-5">
            <h1 className="text-3xl font-bold">Follow Requests</h1>
            <div>
              {followRequests.map((request) => (
                <FollowRequest request={request} />
              ))}
            </div>
          </div>
        </div>
        
    </div>
    </div>
  )
}
