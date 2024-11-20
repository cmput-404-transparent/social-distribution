import Post from "../components/post";
import { useEffect, useState } from "react";

export default function StreamPage() {
  const [posts, setPosts] = useState([]);

  const authorId = localStorage.getItem('authorId');

  useEffect(() => {
    // get posts
    fetch(`${authorId}/stream/`, {
      headers: {
        'Authorization': `Basic ${localStorage.getItem('authToken')}`,
      },
    })
    .then((r) => r.json())
    .then((data) => {
      setPosts(data.results);
    })
  }, [])

  return(
    <div className="page max-h-screen overflow-scroll">
      <div className="flex flex-col space-y-5 items-center w-full">
        {posts.length !== 0? (
          posts.map((post) => (
            <Post post={post} />
          ))
        ) : (
          <div className="flex justify-center items-center h-full">
            <p>No posts yet</p>
          </div>
        )}
      </div>
    </div>
  )
}
