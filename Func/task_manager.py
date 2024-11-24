import globals
import os, time


def reset_tasks():
  globals.tasks={}
  if globals.run==1:
    globals.run=0
  return True

def remove_user_tasks(chat_id):
  if chat_id:
    id=str(chat_id)
    if id in globals.tasks:
      del globals.tasks[id]
      return "Tasks deleted for you!."
    else:
      return "No tasks for you!."
  else:
    return "No User"

def set_tasks(chat_id, tasks):
  if chat_id:
    id=str(chat_id)
    if id in globals.tasks:
      globals[id].extend(tasks)
      return "Tasks Add to task list!.."
    else:
      globals.tasks[id]=tasks
      return "Add to tasks..."
  else:
    return "No user!..."


def add_task(chat_id, task):
  if chat_id:
    id=str(chat_id)
    if id in globals.tasks:
      globals[id].append(task)
      return "Tasks Add to task list!.."
    else:
      globals.tasks[id]=tasks
      return "Add to tasks..."
  else:
    return "No user!..."

def get_tasks_count(chat_id):
  if chat_id:
    id=str(chat_id)
    if id in globals.tasks:
      return len(globals[id])
    else:
      return "No tasks!"
  else:
    return "No user!..."
    

    
