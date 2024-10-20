import { useEffect, useState } from "react"
import getCookie from '../getCSRFToken';
import { marked } from 'marked';
import PeopleIcon from '@mui/icons-material/People';
import LinkIcon from '@mui/icons-material/Link';

const PostState = {
  ViewPost: "ViewPost",
  ModifyPost: "ModifyPost"
};

const Content = ({ post, postState }) => {
  const [title, setTitle] = useState(post.title);
  const [description, setDescription] = useState(post.description);
  const [content, setContent] = useState(post.content);
  const [image, setImage] = useState('')

  useEffect(() => {

    setTitle(post.title);
    setDescription(post.description);
    if (post.contentType === 'text/plain') {
      setContent(post.content);
    }
    else if (post.contentType === 'text/markdown') {
      setContent(post.content);
    }

    else if (post.contentType.includes('image')) {
      setImage(post.content);
      setContent(post.content);
    }
  }, [post])

  const ImageReader = (file) => {
    const reader = new FileReader();
    reader.onloadend = () => {
      setImage(reader.result);
      setContent(reader.result); // If you want to set this as the content
    };
    reader.readAsDataURL(file); // Read the file as base64
  };

  const savePost = async function () {
    console.log("Saving post ");

    const updatedData = {
      title: title,
      description: description,
      content: content,
    };

    const csrftoken = getCookie('csrftoken');
    try {
      await fetch(`/api/authors/${post.author}/posts/${post.id}/`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken,
          'Authorization': `Token ${localStorage.getItem('authToken')}`,
        },
        body: JSON.stringify(updatedData)
      });
    }
    catch (error) {
      console.error('Error:', error);
    }
    window.location.reload();

  }

  const cancelEditPost = async function () {
    window.location.reload();
  }

  if (post.contentType === 'text/plain') {
    return (
      <>
        {/* View Post section */}
        {postState === PostState.ViewPost &&
          <>
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
          </>
        }

        {postState === PostState.ModifyPost &&
          <>
            <div className="p-5">
              <div className="font-bold text-2xl mb-4">
                <input type="text" value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  required
                  className="w-full"
                />
              </div>
              <div className="italic text-neutral-700 mb-4">
                <input type="text" value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  required
                  className="w-full"
                />
              </div>
              <div className="mb-4">
                <textarea type="text" value={content}
                  onChange={(e) => setContent(e.target.value)}
                  required
                  className="w-full"
                ></textarea>
              </div>

              <div className="space-x-3">
                <button
                  onClick={savePost}
                  className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                >Save</button>

                <button
                  onClick={cancelEditPost}
                  className="bg-neutral-500 hover:bg-neutral-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                >Cancel</button>
              </div>
            </div>
          </>
        }
      </>
    )
  }
  else if (post.contentType === 'text/markdown') {
    const postContentHTML = marked(post.content || '');
    return (
      <>
        {postState === PostState.ViewPost &&
          <>
            <div className="p-5">
              <div className="font-bold text-2xl">
                {post.title}
              </div>
              <div className="italic text-neutral-700 pb-3">
                {post.description}
              </div>
              <div>
                {/* Using dangerouslySetInnerHTML to render rich text into HTML 
                  Reference- https://blog.logrocket.com/using-dangerouslysetinnerhtml-react-application/ */}
                <div dangerouslySetInnerHTML={{ __html: postContentHTML }} className="post-content" />
              </div>
            </div>
          </>
        }
        {postState === PostState.ModifyPost &&
          <>
            <div className="p-5">
              <div className="font-bold text-2xl mb-4">
                <input type="text" value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  required
                  className="w-full"
                />
              </div>
              <div className="italic text-neutral-700 mb-4">
                <input type="text" value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  required
                  className="w-full"
                />
              </div>
              <div className="mb-4">
                <textarea type="text" value={content}
                  onChange={(e) => setContent(e.target.value)}
                  required
                  className="w-full"
                ></textarea>
              </div>

              <div className="space-x-3">
                <button
                  onClick={savePost}
                  className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                >Save</button>

                <button
                  onClick={cancelEditPost}
                  className="bg-neutral-500 hover:bg-neutral-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                >Cancel</button>
              </div>
            </div>
          </>
        }
      </>)
  }
  else if (post.contentType.includes('image')) {
    return (
      <>
        {postState === PostState.ViewPost &&
          <>
            <div className="p-5">
              <div className="font-bold text-2xl">
                {post.title}
              </div>
              <div className="italic text-neutral-700 pb-3">
                {post.description}
              </div>
              {/* eslint-disable-next-line */}
              <div className="flex justify-center"><img src={post.content} className="w-1/2" alt="Image Not Found" /></div>

            </div>
          </>
        }
        {postState === PostState.ModifyPost &&
          <>
            <div className="p-5">
              <div className="font-bold text-2xl mb-4">
                <input type="text" value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  required
                  className="w-full"
                />
              </div>
              <div className="italic text-neutral-700 mb-4">
                <input type="text" value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  required
                  className="w-full"
                />
              </div>
              <div className="mb-4">
                <input
                  type="file"
                  accept="image/*"
                  onChange={(e) => ImageReader(e.target.files[0])}
                  required
                  className="w-full"
                />

              </div>

              <div className="space-x-3">
                <button
                  onClick={savePost}
                  className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                >Save</button>

                <button
                  onClick={cancelEditPost}
                  className="bg-neutral-500 hover:bg-neutral-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                >Cancel</button>
              </div>
            </div>
          </>
        }
      </>)
  }
}

export default function Post({ post }) {
  const [author, setAuthor] = useState("");
  const [isStream, setIsStream] = useState(false);
  const [isOwn, setIsOwn] = useState(false);

  const authorId = localStorage.getItem('authorId');
  const [postState, setPostState] = useState(PostState.ViewPost);

  useEffect(() => {
    fetch(`/api/authors/${post.author}/`)
      .then((r) => r.json())
      .then((data) => {
        setAuthor(data);
      });
    setIsStream(window.location.href.includes('stream'));
    setIsOwn(post.author === parseInt(authorId));
    // eslint-disable-next-line
  }, []);

  const dropdown = (e) => {
    const option = e.target.value
    if (option === "edit") {
      Edit()
    }
    else if (option === "delete") {
      Delete()
    }
  }

  const Edit = () => {
    setPostState(PostState.ModifyPost);
    console.log('edit' + post.author)
  }

  const Delete = async () => {
    const csrftoken = getCookie('csrftoken');
    try {
      await fetch(`/api/authors/${post.author}/posts/${post.id}/`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken,
          'Authorization': `Token ${localStorage.getItem('authToken')}`,
        }
      });

    }
    catch (error) {
      console.error('Error:', error);
    }
    window.location.reload();

  }

  return (

    <div className="grid auto-rows-auto grid-flow-row border w-4/5 rounded relative">
      <a href={`/authors/${author.id}`} onClick={!isStream ? (e) => { e.preventDefault() } : null} className={!isStream ? "cursor-default" : "cursor-pointer"}>
        <div className="grid grid-cols-[min-content,auto] auto-cols-auto border-b p-5">
          <div className="pr-8">
            profile picture
          </div>
          <div className="grid grid-flow-row auto-rows-auto space-y-4">
            <div className="grid grid-cols-[auto,auto]">
              <div>
                <h1 className="font-bold text-l">{author.display_name}</h1>
                <h2 className="text-l">@{author.username}</h2>
              </div>
              <div className={post.visibility !== "PUBLIC" && isOwn ? "grid grid-rows-2" : "items-center flex justify-end"}>
                {
                  (!isStream && isOwn) ? (
                    <div>
                      <select id="Dropdown" onChange={dropdown} className="absolute top-2 right-2 border rounded p-1 text-sm">
                        <option>Options</option>
                        <option value="edit">Edit</option>
                        <option value="delete">Delete</option>
                      </select>
                    </div>
                  ) : (<div></div>)
                }
                {
                  ((post.visibility === "FRIENDS") && (
                    <div className="text-right text-neutral-400">
                      FRIENDS ONLY <PeopleIcon className="ml-1" />
                    </div>
                  )) ||
                  ((post.visibility === "UNLISTED") && (
                    <div className="text-right text-neutral-400">
                      UNLISTED <LinkIcon className="ml-1" />
                    </div>
                  ))
                }
              </div>

            </div>

          </div>
        </div>
      </a>
      <Content post={post} postState={postState} />
    </div>
  )
}

