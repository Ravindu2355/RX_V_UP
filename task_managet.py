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
    if globals.tasks[chat_id]:
      del globals.tasks[chat_id]
      return "Tasks deleted for you!."
    else:
      return "No tasks for you!."
  else:
    return "No User"

def set_tasks(chat_id, tasks):
  if chat_id:
    if globals.tasks[chat_id]:
      if globals[chat_id].extend(tasks)
      return "Tasks Add to task list!.."
    else:
      globals.tasks[chat_id]=tasks
      return "Add to tasks..."
  else:
    return "No user!..."


def add_task(chat_id, task):
  if chat_id:
    if globals.tasks[chat_id]:
      if globals[chat_id].append(task)
      return "Tasks Add to task list!.."
    else:
      globals.tasks[chat_id]=tasks
      return "Add to tasks..."
  else:
    return "No user!..."

def get_tasks_count(chat_id):
  if chat_id:
    if globals.tasks[chat_id]:
      return len(globals[chat_id])
    else:
      return "No tasks!"
  else:
    return "No user!..."
    

    
