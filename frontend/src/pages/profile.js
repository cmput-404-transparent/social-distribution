import { useState, useEffect } from "react";
import Post from "../components/post";

export default function Profile() {
  const [profileInfo, setProfileInfo] = useState({});
  const [posts, setPosts] = useState([]);

  const authorId = localStorage.getItem('authorId');

  useEffect(() => {
    // get profile information
    fetch(`/api/authors/${authorId}/`)
    .then((r) => r.json())
    .then((data) => setProfileInfo(data));

    // get posts
    fetch(`/api/authors/${authorId}/posts/`)
    .then((r) => r.json())
    .then((data) => {
      setPosts(data.results);
    })
  }, [])

  return(
    <div className="page">
      <div className="border w-4/5 pt-16">
        <div className="grid grid-flow-row auto-rows-auto space-y-5">
          <div className="grid grid-flow-col grid-cols-2">
            <div className="flex justify-center justify-items-center align-middle">
              <p className="justify-self-center align-middle leading-[inherit]">
                profile picture
              </p>
            </div>
            <div className="grid grid-flow-row auto-rows-auto space-y-4">
              <div>
                <h1 className="font-bold text-3xl">{profileInfo.display_name}</h1>
                <h2>@{profileInfo.username}</h2>
              </div>
              <div className="space-x-3 flex">
                <a href={ `/authors/${authorId}/edit` }>
                  <button type="submit" className='bg-neutral-200 rounded p-2 px-5'>
                    Edit Profile
                  </button>
                </a>
                <button type="submit" className='bg-neutral-200 rounded p-2 px-5'>View Deleted</button>
              </div>
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
