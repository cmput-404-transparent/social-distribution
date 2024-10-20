import { NavLink } from "react-router-dom";
import Post from "../components/post";
import { useEffect, useState } from "react";

export function StreamNavBar() {
  return(
    <div className='grid grid-flow-row auto-rows-max left max-w-max px-[20px] 
            py-[20px] border-r-2 min-h-screen space-y-8'>
      <h1 className='text-sky-400 text-xl font-bold'>Stream</h1>
      <NavLink to="/stream" className="align-middle grid grid-flow-col auto-cols-max">
        <p>Public</p>
      </NavLink>
    </div>
  )
}

export default function StreamPage() {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    // get posts
    fetch(`/api/authors/posts/public/`)
    .then((r) => r.json())
    .then((data) => {
      setPosts(data.posts);
    })
  }, [])

  return(
    <div className="grid grid-cols-[min-content,auto] auto-cols-auto max-h-screen">
      <StreamNavBar />
      <div className="page overflow-scroll">
        <div className="flex flex-col space-y-5 items-center w-full">
          {posts.map((post) => (
            <Post post={post} />
          ))}
        </div>
      </div>
    </div>
  )
}
