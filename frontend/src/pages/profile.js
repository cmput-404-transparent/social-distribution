import { useState, useEffect } from "react";
import Post from "../components/post";
import { useParams } from 'react-router-dom';
import getCookie from "../getCSRFToken";

import Box from '@mui/material/Box';
import CloseIcon from '@mui/icons-material/Close';
import Modal from '@mui/material/Modal';
import { NavLink } from "react-router-dom";
import { ButtonGroup } from "@mui/material";
import { Button } from "@mui/material";
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import {Menu} from "@mui/material";
import {MenuItem} from "@mui/material";

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

export function User({author}) {
  return(
    <NavLink to={author.page} className="cursor-pointer">
      <div className="border rounded my-4 p-4">
        <div className="grid grid-cols-[min-content,auto]">
          <div className="pr-5 flex items-center">
            <p>profile picture</p>
          </div>
          <div className="flex justify-start items-center">
            <h1 className="font-bold text-2xl">{author.displayName}</h1>
          </div>
        </div>
      </div>
    </NavLink>
  )
}


export default function Profile() {
  const [profileInfo, setProfileInfo] = useState({});
  const [posts, setPosts] = useState([]);
  const [relationship, setRelationship] = useState([]);
  const [self, setSelf] = useState(false);

  const [followers, setFollowers] = useState([]);
  const [following, setFollowing] = useState([]);
  const [friends, setFriends] = useState([]);

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
      setPosts(data.posts);
    })

    setSelf(profileAuthorId === authorId);

    fetch(`/api/authors/${authorId}/relationship/${profileAuthorId}`)
    .then((r) => r.json())
    .then((data) => {
      setRelationship(data.relationship)
    });

    // get followers
    fetch(`/api/authors/${profileAuthorId}/followers/`)
    .then((r) => r.json())
    .then((data) => {
      setFollowers(data.followers)
    });

    // get people author follows
    fetch(`/api/authors/${profileAuthorId}/following/`)
    .then((r) => r.json())
    .then((data) => {
      setFollowing(data)
    });

    // get friends of the author
    fetch(`/api/authors/${profileAuthorId}/friends/`)
    .then((r) => r.json())
    .then((data) => {
      setFriends(data.friends)
    });

    setFollowersOpen(false);
    setFollowingOpen(false);
    setFriendsOpen(false);
    

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

  function unfollow() {
    const data = new URLSearchParams();
    data.append('following', profileAuthorId);
    
    const csrftoken = getCookie('csrftoken');

    try {
      fetch(`/api/authors/${authorId}/following/`, {
        method: "DELETE",
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
      console.error('Unfollow user failed:', error);
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

  // for the manage follow menu
  const [anchorEl, setAnchorEl] = useState(null);
  const open = Boolean(anchorEl);
  const clickManageFollowMenu = (event) => {
    setAnchorEl(event.currentTarget);
  };
  const closeManageFollowMenu = () => {
    setAnchorEl(null);
  };

  // for viewing friends modal
  const [friendsOpen, setFriendsOpen] = useState(false);
  const handleFriendsOpen = () => setFriendsOpen(true);
  const handleFriendsClose = () => setFriendsOpen(false);

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
                <h1 className="font-bold text-3xl">{profileInfo.displayName}</h1>
              </div>
              <div className="grid grid-cols-[min-content,min-content,auto] space-x-3 text-left">
                <div onClick={handleFollowersOpen} className="cursor-pointer">
                  <p className="block whitespace-nowrap"><span className="font-bold">{followers.length}</span> Followers</p>
                </div>
                <div onClick={handleFollowingOpen} className="cursor-pointer">
                  <p className="block whitespace-nowrap"><span className="font-bold">{following.length}</span> Following</p>
                </div>
                <div onClick={handleFriendsOpen} className="cursor-pointer">
                  <p className="block whitespace-nowrap"><span className="font-bold">{friends.length}</span> Friends</p>
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
                  relationship === "NONE"? (
                    <div className="space-x-3 flex">
                      <button className='bg-sky-400 rounded p-2 px-5' onClick={follow}>
                        Follow
                      </button>
                    </div>
                  ) : (
                    <div className="space-x-3 flex">
                      <ButtonGroup variant="contained" aria-label="Basic button group">
                        <Button className="!drop-shadow-none !bg-neutral-200 !text-black !border-none" disabled disableElevation>{relationship}</Button>
                        <Button className="!drop-shadow-none !bg-neutral-200 !text-black" id="manage-follow-btn" disableElevation onClick={clickManageFollowMenu}>
                          <KeyboardArrowDownIcon />
                        </Button>
                      </ButtonGroup>
                      <Menu anchorEl={anchorEl} open={open} onClose={closeManageFollowMenu} MenuListProps={{ 'aria-labelledby': 'manage-follow-btn' }}>
                        <MenuItem onClick={unfollow}>Unfollow</MenuItem>
                      </Menu>
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
              <User author={follower} />
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
              <User author={followingUser} onClick={handleFollowingClose} />
            ))}
          </div>
        </Box>
      </Modal>

      {/* friends modal */}
      {/**
       * source: Material UI Documentation
       * link: https://mui.com/material-ui/react-modal/
       * date: October 20, 2024
       */}
      <Modal
        open={friendsOpen}
        onClose={handleFriendsClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box sx={style}>
          <div className="grid grid-cols-2">
            <h2 className="font-bold text-3xl">
              Friends
            </h2>
            <div className="flex justify-end">
              <CloseIcon sx={{ color: '#bbb' }} onClick={handleFriendsClose} className="cursor-pointer" />
            </div>
            
          </div>
          <div>
            {friends.map((friend) => (
              <User author={friend} onClick={handleFriendsClose} />
            ))}
          </div>
        </Box>
      </Modal>
    </div>
  );
};
