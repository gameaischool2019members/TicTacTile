# Lily's Garden Simulator

The Linux simulator build can be run inside a Docker container. Please follow instructions below to build and run the Docker image.

## Build
    docker build -t lg-simulator .
    
## Run
    docker run -p 8090:8080 -it lg-simulator
    
## Ping
Test that the simulator server is running by visiting the following URL:

    curl http://localhost:8090/ping
    
It should respond with `Pong`

## List Running Containers
	docker ps

## Tail Log
    docker exec CONTAINER_ID tail -f "/root/.config/unity3d/Tactile Entertainment/Lilys Garden/Player.log"
    
### E.g.
    
    docker exec 29b8331df475 tail -f "/root/.config/unity3d/Tactile Entertainment/Lilys Garden/Player.log"
    
    
## HTTP API

All endpoints, except `ping` should be called using the HTTP POST method.

### Ping

* URL: `/ping`
* Input: N/A
* Output: `Pong`

### Load level

* URL: `/load`
* Input: `levelIndex:int`, `seed:int`
* Output: `state:string`, `stateSparse:string`

### Click piece

* URL: `/click`
* Input: `state:string`, `x:int`, `y:int`
* Output: `clickSuccessful:bool`, `simulationResult:string`, `state:string`

### Session create

* URL: `/session/create`
* Input: `state:string`
* Output: `sessionId:string`, `sparseState:string`

### Session click

* URL: `/session/click`
* Input: `sessionId:string`, `x:int`, `y:int`
* Output: `clickSuccessful:bool`, `simulationResult:string`, `sparseState:string`

### Session status

* URL: `/session/status`
* Input: `sessionId:string`
* Output: `state:string`, `stateSparse:string`

### Session destroy

* URL: `/session/destroy`
* Input: `sessionId:string`
* Output: `destroyed:book`

### Sessions list

* URL: `/sessions/list`
* Input: N/A
* Output: `sessionIds:array<string>`

### Sessions clear

* URL: `/sessions/clear`
* Input: N/A
* Output: `sessionIds:array<string>` (always empty)