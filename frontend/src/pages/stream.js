import Post from "../components/post";
import { useEffect, useState } from "react";

export default function StreamPage() {
  const [posts, setPosts] = useState([]);

  const authorId = localStorage.getItem('authorId');

  useEffect(() => {
    // get posts
    fetch(`/api/authors/${authorId}/stream/`)
    .then((r) => r.json())
    .then((data) => {
      setPosts(data.results);
    })
  }, [])

  return(
    <div className="page max-h-screen overflow-scroll">
      <div className="flex flex-col space-y-5 items-center w-full">
        {posts.map((post) => (
          <Post post={post} />
        ))}
      </div>
    </div>
  )
}
