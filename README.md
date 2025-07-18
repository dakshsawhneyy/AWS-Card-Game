# AWS-Card-Game

Don't have physical cards to play with friends? No problem.
I built **AWS-Card-Game** - a fully serverless, production-grade, multiplayer card game using over 20 AWS services. I lost count. Maybe you can count. From real-time game state, live health tracking, multiplayer turn logic, in-game chat, automated pipelines, to secured deployments - this is not a side project. This is a cloud-native engineering achievement.

I didn’t just build a game.
I engineered a real-time, cloud-scalable multiplayer experience - with CI/CD, observability, IAM-tightened security, real-time chat, fault tolerance, and stateful persistence - all in AWS. This is what happens when DevOps meets game logic.

---

## 🧝🏻‍♀️ Architecture Breakdown

###  Backend (Fully Serverless)
- **Lambda Functions**: Handle every single action - from `throwCard`, `endGame`, `startGame`, `attackPlayer`, `sendMessage`, etc.
- **API Gateway**: Expose all backend Lambda endpoints as RESTful APIs.
- **DynamoDB**:
  - `games` table: Tracks all live and ended games.
  - `players` table: Stores current player states, health, turns.
  - `gameChatMessages`: Real-time player messages.
- **WebSocket API Gateway**: For future real-time gameplay and live updates.

###  Frontend
- Built in **React** and hosted on **AWS Amplify + S3 Static Hosting**
- Responsive UI with:
  - Game screen with player cards, game logs, scoreboard.
  - Chat section component to talk with other players live.
  - Buttons: attack, throw, heal, end game.

###  CI/CD & Automation
- **CodePipeline** + **CodeBuild**: Push your code and it deploys - frontend, backend, Lambda packages, all automated.
- **CloudFormation**: Infra-as-code, redeploy the whole setup in minutes.

### Monitoring & Logs
- **CloudWatch**: Full visibility into every player move, attack, throwCard.
- Game logic outputs structured logs, ready for log-based dashboards.
- **Athena + QuickSight (planned)**: For gameplay analytics and leaderboard insights.

### In-Game Chat Feature
**Phase 8: Extra Magic** - Chat section implemented between players, live and stored via:
- **Lambda**: `sendMessageToGame`, `getMessagesForGame`
- **API Gateway**: REST APIs connected to chat functions
- **DynamoDB Table**: `gameChatMessages` for storing timestamped messages per game
- Clean UI component for players to interact live

---

## 📈 Phased Development (like Game Levels)

| Phase | Goal                            | AWS Skills Focus                                 |
|-------|----------------------------------|--------------------------------------------------|
| 1     | Concept & Design                | System Design, Planning                          |
| 2     | Basic Backend Setup             | Lambda, API Gateway, DynamoDB                    |
| 3     | Frontend & User Interaction     | Amplify, S3 Static Hosting, Cognito              |
| 4     | Game State & Realtime           | WebSocket, DynamoDB Streams, SNS (future)        |
| 5     | Scoreboard & Analytics          | CloudWatch, Athena, QuickSight                   |
| 6     | Security & Auth                 | IAM, Secrets Manager                             |
| 7     | Automation & Deployment         | CloudFormation, CodePipeline, CodeBuild          |
| 8     | Extra Magic                     | Lambda Chat System, Game Logging, Live UX Boost  |

---

## What Makes It Jawdropping?
- Over 100 commits of raw engineering and logic.
- Serverless multiplayer gameplay.
- Real-time player state management.
- In-game chat between players.
- CI/CD Pipeline integrated with multiple environments.
- Designed like a real product, not a pet project.
- Zero hardcoded nonsense. Everything scalable.

---

## Tech Stack
- **Frontend**: React.js, AWS Amplify, S3
- **Backend**: Node.js Lambda functions, API Gateway
- **Database**: DynamoDB (3 tables)
- **CI/CD**: CodePipeline, CodeBuild
- **Security**: Cognito, IAM, WAF, Secrets Manager
- **Monitoring**: CloudWatch Logs + Alarms
- **Chat System**: Lambda + API Gateway + DynamoDB

---

##  Final Thought
This isn’t just a card game. It’s an entire AWS ecosystem fused with game logic, CI/CD, scalability, and real-time cloud-native magic.

Play it, deploy it, break it, or hire me to build your next one.

