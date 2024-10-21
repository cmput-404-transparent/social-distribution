import { TextField } from "@mui/material";
import {Button} from "@mui/material";
import SearchIcon from '@mui/icons-material/Search';
import { useState } from "react";
import { NavLink } from "react-router-dom";

export function AuthorResult({author}) {
  return(
    <NavLink to={`/authors/${author.id}`} className="cursor-pointer">
      <div className="border rounded my-4 p-4">
        <div className="grid grid-cols-[min-content,auto]">
          <div className="pr-5 flex items-center">
            <p>profile picture</p>
          </div>
          <div>
            <h1 className="font-bold text-2xl">{author.display_name}</h1>
            <h2>@{author.username}</h2>
          </div>
        </div>
      </div>
    </NavLink>
  )
}

export default function Search() {
  const [keyword, setKeyword] = useState("");
  const [results, setResults] = useState([]);

  const searchAuthors = (e) => {
    e.preventDefault();

    const data = new URLSearchParams();
    data.append('keyword', keyword);

    fetch(`/api/authors/search/?keyword=${data}`)
    .then((r) => r.json())
    .then((data) => {
      setResults(data);
    })
  }

  return(
    <div className="page">
      <div className="w-5/6 flex justify-center">
        <div className="grid grid-rows-[min-content,min-content] w-3/4">
          <h1 className="font-bold text-xl pb-3">Find Authors</h1>
          <form className="grid grid-cols-[auto,min-content] auto-cols-auto w-full space-x-4" onSubmit={searchAuthors}>
            <TextField id="outlined-search" label="Search" type="search" className="w-full" onChange={(e) => setKeyword(e.target.value)}/>
            <Button variant="contained" type="submit"><SearchIcon /></Button>
          </form>
          <div className="search-results">
            {results.map((author) => (
              <AuthorResult author={author} />
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
