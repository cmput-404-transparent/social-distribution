import { useEffect, useState } from "react"

function content(post) {
  // plain text post
  if (post.contentType == 'text/plain') {
    return(
      <div className="p-5">
        <div className="font-bold text-2xl">
          {post.title}
        </div>
        <div className="italic text-neutral-700 pb-3">
          {post.description}
        </div>
        <div>
          {post.content}
        </div>
      </div>
    )
  }
  else if (post.contentType == 'text/markdown') {
    return(
      <div className="p-5">
        <div className="font-bold text-2xl">
          {post.title}
        </div>
        <div className="italic text-neutral-700 pb-3">
          {post.description}
        </div>
        <div>
          {/* TODO: implement markdown */}
          {post.content}
        </div>
      </div>
    )
  }
}

export default function Post({ post }) {
  const [author, setAuthor] = useState("");
  
  useEffect(() => {
    fetch(`/api/authors/${post.author}/`)
    .then((r) => r.json())
    .then((data) => {
      setAuthor(data);
    })
  }, []);

  return(
    <div className="grid auto-rows-auto grid-flow-row border w-4/5 rounded">
      <div className="grid grid-cols-[min-content,auto] auto-cols-auto border-b p-5">
        <div className="pr-8">
          profile picture
        </div>
        <div className="grid grid-flow-row auto-rows-auto space-y-4">
          <div>
            <h1 className="font-bold text-l">{author.display_name}</h1>
            <h2 className="text-l">@{author.username}</h2>
          </div>
        </div>
      </div>
      {content(post)}
    </div>
  )
}
