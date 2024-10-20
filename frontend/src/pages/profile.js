import { useState, useEffect } from "react";
import Post from "../components/post";
import { useParams } from 'react-router-dom';
import getCookie from "../getCSRFToken";

export default function Profile() {
  const [profileInfo, setProfileInfo] = useState({});
  const [posts, setPosts] = useState([]);
  const [self, setSelf] = useState(false);

  const authorId = localStorage.getItem('authorId');
  const { profileAuthorId } = useParams();

  useEffect(() => {
    // get profile information
    fetch(`/api/authors/${profileAuthorId}/`)
    .then((r) => r.json())
    .then((data) => setProfileInfo(data));

    // get posts
    fetch(`/api/authors/${profileAuthorId}/posts/`)
    .then((r) => r.json())
    .then((data) => {
      setPosts(data.results);
    })

    setSelf(profileAuthorId === authorId);
    // eslint-disable-next-line
  }, [profileAuthorId]);

  function follow() {

    const data = new URLSearchParams();
    data.append('user', profileAuthorId);
    data.append('follower', authorId);
    const csrftoken = getCookie('csrftoken');

    try {
      fetch("/api/authors/follow/", {
        method: "POST",
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': csrftoken,
        },
        body: data.toString(),
      })
      .then((r) => {
        window.location.reload();
      });
    } catch (error) {
      console.error('Follow user failed:', error);
    }
  }

  return(
    <div className="page overflow-scroll max-h-screen">
      <div className="w-4/5 pt-16">
        <div className="grid grid-flow-row auto-rows-auto space-y-5">
          <div className="grid grid-flow-col grid-cols-2">
            <div className="flex justify-center justify-items-center align-middle">
              <p className="items-center justify-center flex">
                profile picture
              </p>
            </div>
            <div className="grid grid-flow-row auto-rows-auto space-y-4">
              <div>
                <h1 className="font-bold text-3xl">{profileInfo.display_name}</h1>
                <h2>@{profileInfo.username}</h2>
              </div>
              <div className="grid grid-cols-[min-content,auto] space-x-3 text-left">
                <div>
                  <p className="block whitespace-nowrap"><span className="font-bold">{profileInfo.followers}</span> Followers</p>
                </div>
                <div>
                <p className="block whitespace-nowrap"><span className="font-bold">{profileInfo.following}</span> Following</p>
                </div>
              </div>
              {
                self? (
                  <div className="space-x-3 flex">
                    <a href={ `/authors/${authorId}/edit` }>
                      <button type="submit" className='bg-neutral-200 rounded p-2 px-5'>
                        Edit Profile
                      </button>
                    </a>
                    <button type="submit" className='bg-neutral-200 rounded p-2 px-5'>View Deleted</button>
                  </div>
                ) : (
                  profileInfo.relationship === "NONE"? (
                    <div className="space-x-3 flex">
                      <button className='bg-sky-400 rounded p-2 px-5' onClick={follow}>
                        Follow
                      </button>
                    </div>
                  ) : (
                    <div className="space-x-3 flex">
                      <button className='bg-neutral-200 rounded p-2 px-5' disabled>
                        {profileInfo.relationship}
                      </button>
                    </div>
                  )
                  
                )
              }
            </div>
          </div>
          <div className="flex flex-col space-y-5 items-center">
            {posts.map((post) => (
              <Post post={post} />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
