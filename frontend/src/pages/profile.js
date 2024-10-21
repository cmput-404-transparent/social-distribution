import { useState, useEffect } from "react";
import Post from "../components/post";
import { useParams } from 'react-router-dom';
import getCookie from "../getCSRFToken";

import Box from '@mui/material/Box';
import CloseIcon from '@mui/icons-material/Close';
import Modal from '@mui/material/Modal';
import { AuthorResult } from "./search";

/**
  * source: Material UI Documentation
  * link: https://mui.com/material-ui/react-modal/
  * date: October 20, 2024
  */
const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: '40%',
  bgcolor: 'background.paper',
  borderRadius: "0.25rem",
  p: 4
};


export default function Profile() {
  const [profileInfo, setProfileInfo] = useState({});
  const [posts, setPosts] = useState([]);
  const [self, setSelf] = useState(false);
  const [followers, setFollowers] = useState([]);
  const [following, setFollowing] = useState([]);

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

    // get followers
    fetch(`/api/authors/${profileAuthorId}/followers/`)
    .then((r) => r.json())
    .then((data) => {
      setFollowers(data)
    });

    // get people author follows
    fetch(`/api/authors/${profileAuthorId}/following/`)
    .then((r) => r.json())
    .then((data) => setFollowing(data));

    setFollowersOpen(false);
    setFollowingOpen(false);

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

  // for viewing followers modal
  const [followersOpen, setFollowersOpen] = useState(false);
  const handleFollowersOpen = () => setFollowersOpen(true);
  const handleFollowersClose = () => setFollowersOpen(false);

  // for viewing following modal
  const [followingOpen, setFollowingOpen] = useState(false);
  const handleFollowingOpen = () => setFollowingOpen(true);
  const handleFollowingClose = () => setFollowingOpen(false);

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
                <div onClick={handleFollowersOpen} className="cursor-pointer">
                  <p className="block whitespace-nowrap"><span className="font-bold">{profileInfo.followers}</span> Followers</p>
                </div>
                <div onClick={handleFollowingOpen} className="cursor-pointer">
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

      {/* followers modal */}
      {/**
       * source: Material UI Documentation
       * link: https://mui.com/material-ui/react-modal/
       * date: October 20, 2024
       */}
      <Modal
        open={followersOpen}
        onClose={handleFollowersClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box sx={style}>
          <div className="grid grid-cols-2">
            <h2 className="font-bold text-3xl">
              Followers
            </h2>
            <div className="flex justify-end">
              <CloseIcon sx={{ color: '#bbb' }} onClick={handleFollowersClose} className="cursor-pointer" />
            </div>
            
          </div>
          <div>
            {followers.map((follower) => (
              <AuthorResult author={follower} />
            ))}
          </div>
        </Box>
      </Modal>

      {/* following modal */}
      {/**
       * source: Material UI Documentation
       * link: https://mui.com/material-ui/react-modal/
       * date: October 20, 2024
       */}
      <Modal
        open={followingOpen}
        onClose={handleFollowingClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box sx={style}>
          <div className="grid grid-cols-2">
            <h2 className="font-bold text-3xl">
              Following
            </h2>
            <div className="flex justify-end">
              <CloseIcon sx={{ color: '#bbb' }} onClick={handleFollowingClose} className="cursor-pointer" />
            </div>
            
          </div>
          <div>
            {following.map((followingUser) => (
              <AuthorResult author={followingUser} onClick={handleFollowingClose} />
            ))}
          </div>
        </Box>
      </Modal>
    </div>
  );
};
