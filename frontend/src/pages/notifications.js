import { useEffect, useState } from "react";
import getCookie from "../getCSRFToken";
import { PostProfilePicture } from "../components/profilePicture";

function FollowRequest({request, authorId}) {

  const csrftoken = getCookie('csrftoken');
  
  function accept() {
    const data = new URLSearchParams();
    data.append('follower', request.id);

    try {
      fetch(`/api/authors/${authorId}/follow_request/`, {
        method: "PUT",
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': csrftoken,
        },
        body: data.toString()
      })
      .then((response) => {
        if (response.ok) {
          window.location.reload();
        } else {
          alert("accept follow failed");
        }
      })
    } catch (error) {
      console.log("error accepting follow request:", error);
    }
    
  }

  function remove() {
    const data = new URLSearchParams();
    data.append('follower', request.id);

    try {
      fetch(`/api/authors/${authorId}/follow_request/`, {
        method: "DELETE",
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': csrftoken,
        },
        body: data.toString()
      })
      .then((response) => {
        if (response.ok) {
          window.location.reload();
        } else {
          alert("delete follow request failed");
        }
      })
    } catch (error) {
      console.log("error deleting follow request:", error);
    }
    
  }

  return(
    <div className="border rounded">
      <div className="grid grid-cols-[auto,auto] auto-cols-auto border-b p-5">
        <a href={`/authors/${request.id}`}>
          <div className="grid grid-cols-[min-content,auto]">
            <div className="pr-8">
              <PostProfilePicture displayName={request.display_name} imageURL={request.profile_image}/>
            </div>
            <div className="flex flex-col justify-center">
              <h1 className="font-bold text-l">{request.display_name}</h1>
              <h2 className="text-l">@{request.username}</h2>
            </div>
          </div>
        </a>
        <div className="grid grid-cols-1">
          <div className="space-x-2 flex justify-end">
            <button type="submit" className='bg-customOrange rounded p-2 px-4' onClick={accept}>Accept</button>
            <button type="submit" className='bg-neutral-200 rounded p-2 px-4' onClick={remove}>Delete</button>
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
    // eslint-disable-next-line
  }, [])

  return (
    <div className="page">
      <div className="w-5/6 justify-center flex">
        <div className="grid grid-flow-row auto-rows-auto w-3/4">
          <div className="grid grid-rows-[min-content,auto] space-y-5">
            <h1 className="text-3xl font-bold">Follow Requests</h1>
            <div>
              {followRequests.map((request) => (
                <FollowRequest request={request} authorId={authorId} />
              ))}
            </div>
          </div>
        </div>
        
    </div>
    </div>
  )
}
