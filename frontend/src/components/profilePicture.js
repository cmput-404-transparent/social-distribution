
export function ProfilePicture({ displayName, imageURL }) {
  return(
    <div class="flex items-center justify-center space-x-8">
      {
        imageURL? (
          <img src={imageURL} className="w-32 h-32 rounded-full flex justify-center"></img>
        ) : (
          <div className="w-32 h-32 bg-customLightBlue rounded-full flex justify-center items-center text-center text-5xl">
            {displayName? (
              displayName[0]
            ): ''}
          </div>
        )
      }
    </div>
  )
}

export function PostProfilePicture({ displayName, imageURL }) {
  return(
    <div class="flex items-center justify-center space-x-8">
      {
        imageURL? (
          <img src={imageURL} className="w-16 h-16 min-w-16 min-h-16 rounded-full flex justify-center"></img>
        ) : (
          <div className="w-16 h-16 bg-customLightBlue rounded-full flex justify-center items-center text-center text-2xl">
            {displayName? (
              displayName[0]
            ): ''}
          </div>
        )
      }
    </div>
  )
}
