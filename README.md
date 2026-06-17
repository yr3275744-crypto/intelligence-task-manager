## System description

Agent and task management system for the ShadowNet unit.

## Folder structure

intelligence-task-manager/

|- database

| |- db_connection

| |- agent_db

| |- mission_db

|- README.md

|- requirements.txt

|- .gitignore

## Table structure

### agents table

- id: INT, AUTO_INCREMENT, PRIMARY KEY

- name: VARCHAR, NOT NULL

- specialty: VARCHAR, NOT NULL

- is_active: BOOLEAN, DEFAULT TRUE

- completed missions: INT, DEFAULT 0

- failed missions: INT, DEFAULT 0

- agent_rank: ENUM (Junior, Senior, Commander)

### missions TABLE

- id: INT, AUTO_INCREMENT, PRIMARY KEY

- title: VARCHAR, NOT NULL

- description: TEXT, NOT NULL

- location: VARCHAR, NOT NULL

- difficulty: INT (1 - 10), NOT NULL

- importance: INT (1 - 10), NOT NULL

- status: VARCHAR, DEFAULT NEW

- risk level: VARCHAR, NOT NULL

- assigned agent id: INT, DEFAULT NULL

## DBConnection, AgentDB and MissionDB classes

### DBConnection

Create connection with the database and create the tables.

methods:
- get_connection():
return connection to the mysql

- create_database():
create the Intelligence_db if not exists

- creatr_tables():
create the tables if not exists

### AgentDB

Responsible for all SQL operations against the agents table.

methods:

- create_agent(data):
create new agent and return it

- get_all_agents():
return all of agants

- get_agent_by_id(id):
return agent by id or None

- update_agent(id, data):
update all the line

- deactivate_agent(id):
deactivate an agent

- increment_completted(id):
Updates the number of tasks completed.

- increment_failed(id):
Updates the number of tasks failed.

- ge_agent_performance(id):
returm dict with keyes total, failed, completed, success_rate

- count_active_agents():
Returns the number of active agents

### MissionDB

Responsible for all SQL operations against the missions table.

methods:

- create_mision(data):
create new mission and return it

- get_all_missions():
returm all of the missions

- get_mission_by_id(id):
return nision by id

- assign_mission(m_id, a_id):
assign mission to an agen

- get_open_missions_by_agent(id):
return ASSIGNED / IN PROGRESS missions of an agent

- count_all_missions():
count all missions

- count_by_status():
count by status

- count_open_missions():
count open missions

- count_critical_missions():
count critical missions

- get_top_agent():
return the agent with the highst comleted missions number

## System rules

- rank must be Commander / Senior / Junior — any other value throws an error.

- Difficulty and importance must be between 1 and 10 — otherwise an error.

- vel_risk is calculated automatically when a task is created—the user does not submit it.

- An agent with False=active_is cannot receive tasks.

- An agent cannot have more than 3 open tasks (PROGRESS_IN / ASSIGNED) at the same time.

- If CRITICAL=level_risk — only an agent with the rank of Commander can accept the mission.

- Only a task with a status of NEW can be assigned. After assignment: .ASSIGNED=status

- Only a task with the ASSIGNED status can be started. After: .PROGRESS_IN=stat

- Only a task can be completed. PROGRESS_IN and changed to completed or failed status.

- Only a task with a status of NEW or ASSIGNED can be canceled — otherwise an error.

## Running instructions

in cmd: 

run doker:

```docker run -d --name intelligence-mysql -e MYSQL_ROOT_PASSWORD=1234 -e MYSQL_DATABASE=Intelligence_db -p 3306:3306 mysql:8.0```

clone the project to a folder:

```git clone https://github.com/yr3275744-crypto/intelligence-task-manager.git```

create venv:

```py -m venv .venv```

```.\.venv\Scripts\activate```

install the requirements:

```py -m pip install requirements.txt```

play the db files:

```py .\database\db_connection.py```

```py -m database.agent_db```

```py -m database.mission_db```