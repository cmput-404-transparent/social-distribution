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
import {PostProfilePicture, ProfilePicture} from "../components/profilePicture";

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
            <PostProfilePicture displayName={author.displayName} imageURL={author.profileImage} />
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
  const [relationship, setRelationship] = useState("NONE");

  const [followers, setFollowers] = useState([]);
  const [following, setFollowing] = useState([]);
  const [friends, setFriends] = useState([]);

  const authorId = localStorage.getItem('authorId');
  const { profileAuthorId } = useParams();

  useEffect(() => {
    // get profile information
    const host = window.location.origin;
    localStorage.setItem('host', host);
    fetch(`/api/authors/${profileAuthorId}/`, {
      headers: {
        'Authorization': `Basic ${localStorage.getItem('authToken')}`,
      },
    })
    .then((r) => r.json())
    .then((data) => setProfileInfo(data));

    setFollowersOpen(false);
    setFollowingOpen(false);
    setFriendsOpen(false);

    // eslint-disable-next-line
  }, [profileAuthorId]);

  useEffect(() => {
    if (Object.keys(profileInfo).length !== 0) {
      // get posts
      alert(profileInfo.id);
      alert(profileInfo.id.startsWith(localStorage.getItem('host')));
      const url =profileInfo.host
      url = url.replace("/api/", "");
      if (profileInfo.id.startsWith(localStorage.getItem('host'))=== false) {
        fetch(`${localStorage.getItem('host')}/remote-nodes/?host=${url}}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          }
        })
        .then((response) => response.json())
        .then((data) => {
          const { username, password } = data;
          const authString = `${username}:${password}`;
          const encodedAuth = btoa(authString);
          localStorage.setItem('remoteAuth', encodedAuth);
        })
        .catch((error) => {
          console.error('Error fetching remote nodes:', error);
        });
        fetch(`${profileInfo.id}/posts/`, {
          headers: {
            'Authorization': `Basic ${localStorage.getItem('encodedAuth')}`,
          },
          })
          .then((r) => r.json())
          .then((data) => {
            setPosts(data.posts);
          })
      }
      else {
        fetch(`${profileInfo.id}/posts/`, {
          headers: {
            'Authorization': `Basic ${localStorage.getItem('authToken')}`,
          },
          })
          .then((r) => r.json())
          .then((data) => {
            setPosts(data.posts);
          })
      }

 

      fetch(`${authorId}/relationship/${profileAuthorId}/`, {
        headers: {
          'Authorization': `Basic ${localStorage.getItem('authToken')}`,
        },
      })
      .then((r) => r.json())
      .then((data) => {
        setRelationship(data.relationship);
      });

      // get followers
      fetch(`${profileInfo.id}/followers/`, {
        headers: {
          'Authorization': `Basic ${localStorage.getItem('authToken')}`,
        },
      })
      .then((r) => r.json())
      .then((data) => {
        setFollowers(data.followers)
      });

      // get people author follows
      fetch(`${profileInfo.id}/following/`, {
        headers: {
          'Authorization': `Basic ${localStorage.getItem('authToken')}`,
        },
      })
      .then((r) => r.json())
      .then((data) => {
        setFollowing(data)
      });

      // get friends of the author
      fetch(`${profileInfo.id}/friends/`, {
        headers: {
          'Authorization': `Basic ${localStorage.getItem('authToken')}`,
        },
      })
      .then((r) => r.json())
      .then((data) => {
        setFriends(data.friends)
      });
    }
  }, [profileInfo]);

  function follow() {

    const data = new URLSearchParams();
    data.append('user', profileAuthorId);
    data.append('follower', authorId.split("/").pop());
    const csrftoken = getCookie('csrftoken');

    try {
      fetch("/api/authors/follow/", {
        method: "POST",
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': csrftoken,
          'Authorization': `Basic ${localStorage.getItem('authToken')}`,
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
      fetch(`${authorId}/following/`, {
        method: "DELETE",
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': csrftoken,
          'Authorization': `Basic ${localStorage.getItem('authToken')}`,
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
                <ProfilePicture displayName={profileInfo.displayName} imageURL={profileInfo.profileImage} />
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
                relationship === "SELF" ? (
                  <div className="space-x-3 flex">
                    <a href={ `/authors/${authorId.split("/").pop()}/edit` }>
                      <button type="submit" className='bg-customOrange rounded p-2 px-5'>
                        Edit Profile
                      </button>
                    </a>
                  </div>
                ) : (
                  relationship === "NONE"? (
                    <div className="space-x-3 flex">
                      <button className='bg-customOrange rounded p-2 px-5' onClick={follow}>
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
                        <MenuItem onClick={unfollow}>
                          {relationship === "REQUESTED"? (
                            <p>Cancel</p>
                          ) : (
                          <p>Unfollow</p>
                          )}
                        </MenuItem>
                      </Menu>
                    </div>
                  )
                )
              }
            </div>
          </div>
          <div className="flex flex-col space-y-5 items-center min-h-full">
            {posts.length !== 0? (
              posts.map((post) => (
                <Post post={post} />
              ))
            ) : (
              <div className="flex justify-center items-center min-h-full">
                <p>No posts yet</p>
              </div>
            )}
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
            {followers.length !== 0? (
              followers.map((follower) => (
                <User author={follower} />
              ))
            ) : (
              <p>No followers yet</p>
            )}
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
            {following.length !== 0? (
              following.map((followingUser) => (
                <User author={followingUser} onClick={handleFollowingClose} />
              ))
            ) : (
              <p>Not following anyone yet</p>
            )}
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
            {friends.length !== 0? (
              friends.map((friend) => (
                <User author={friend} onClick={handleFriendsClose} />
              ))
            ) : (
              <p>No friends yet</p>
            )}
          </div>
        </Box>
      </Modal>
    </div>
  );
};
