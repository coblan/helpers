from helpers.director.shortcut import model_to_name, model_full_permit, add_permits, model_read_permit
from .models import SystemMessage

permits=[
    
    ('SystemMessage',model_read_permit(SystemMessage),model_to_name(SystemMessage),'model'),
  
    ]
add_permits(permits)

