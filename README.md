![](https://github.com/cmput-404-transparent/social-distribution/blob/main/images/social-distribution-banner.jpg)

# SocialDistribution </> <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" /> <img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue" />
A decentralized social blogging platform that enables users to share posts and aggregate content from other sources, using a simple, RESTful inbox model.

<p align="center"><img src="https://github.com/cmput-404-transparent/social-distribution/blob/main/images/sample-stream-screenshot.png" width="375"/> <img src="https://github.com/cmput-404-transparent/social-distribution/blob/main/images/sample-profile-screenshot.png" width="375" /></p>

## Features 🌟
- <b>Distributed Social Network:</b> Allows users to interact across different nodes, maintaining autonomy while sharing posts and content.
- <b>Inbox Model:</b> Posts, likes, and comments are routed through an inbox system, ensuring that content is shared with the appropriate users (public posts to followers, friends-only posts to specific users).
- <b>Content Aggregation:</b> Users can aggregate posts from authors they follow across different nodes, creating a personalized feed.
- <b>RESTful Architecture:</b> The platform is built with a simple, RESTful architecture, focusing on ease of use and scalability without complex protocols like ActivityPub.
- <b>User-Friendly:</b> Designed to be intuitive and easy to navigate, making it simple for users to interact with posts, like and comment, and manage their content without a steep learning curve.

## Requirements 📋
SocialDistribution requires <a href="https://www.python.org/downloads/">Python</a> 3.11+ and <a href="https://nodejs.org/en/download/package-manager">Node.js</a> 20+ to run.

## Install ⚙️
To install dependencies, run the following command.
```bash  
make dependencies  
```

## Running Locally 🚀
To run the webapp, first create a production build of the frontend.
```bash
make build
```
Then, run the Django server.
```bash
make backend
```

## Documentation 📚
To view documentation for API endpoints, run the Django server, and visit `/redoc/`.

## Testing 🧪
To ensure the reliability and functionality of the backend, unit tests have been written using Django's testing framework. These tests cover various parts of the application, including model logic, views, and API endpoints.

To run them, execute the following command.
```bash
make test
```

## Deployed Nodes 🌐
The following are our nodes that are already deployed on Heroku.
1. [https://social-distribution-tqyoung-bad8770cc2df.herokuapp.com/](https://social-distribution-tqyoung-bad8770cc2df.herokuapp.com/)
2. [https://transparent-jwan-de425e3e313f.herokuapp.com/](https://transparent-jwan-de425e3e313f.herokuapp.com/)
3. [https://social-distribution-omelchuk-a7deff81f6a3.herokuapp.com/](https://social-distribution-omelchuk-a7deff81f6a3.herokuapp.com/ )
4. [https://social-distribution-asolanki-45d4887bf9b6.herokuapp.com/](https://social-distribution-asolanki-45d4887bf9b6.herokuapp.com/)
5. [https://jastegh-socialdistribution-c7853f320baf.herokuapp.com/](https://jastegh-socialdistribution-c7853f320baf.herokuapp.com/)
6. [https://socialdistribution-jassidak-a0db46597407.herokuapp.com/](https://socialdistribution-jassidak-a0db46597407.herokuapp.com/)

## Contributors 👩‍💻
<div>  
<a href="https://github.com/Maia580"><img src="https://images.weserv.nl/?url=https://github.com/Maia580.png?v=4&h=50&w=50&fit=cover&mask=circle&maxage=7d"/></a>
<a href="https://github.com/hamsandvich"><img src="https://images.weserv.nl/?url=https://github.com/hamsandvich.png?v=4&h=50&w=50&fit=cover&mask=circle&maxage=7d"/></a>
<a href="https://github.com/Abhi1410-lab"><img src="https://images.weserv.nl/?url=https://github.com/Abhi1410-lab.png?v=4&h=50&w=50&fit=cover&mask=circle&maxage=7d"/></a>
<a href="https://github.com/Jastegh"><img src="https://images.weserv.nl/?url=https://github.com/Jastegh.png?v=4&h=50&w=50&fit=cover&mask=circle&maxage=7d"/></a>
<a href="https://github.com/jassidaksingh"><img src="https://images.weserv.nl/?url=https://github.com/jassidaksingh.png?v=4&h=50&w=50&fit=cover&mask=circle&maxage=7d"/></a>
<a href="https://github.com/tammy-young"><img src="https://images.weserv.nl/?url=https://github.com/tammy-young.png?v=4&h=50&w=50&fit=cover&mask=circle&maxage=7d"/></a>
</div>  

## Contributing 🤝
Contributions are welcome! Please open an issue or submit a pull request. Make sure to follow the coding standards outlined in the repository.

## License 📜
This project is licensed under the [Apache 2.0 License](https://github.com/cmput-404-transparent/social-distribution?tab=Apache-2.0-1-ov-file).
