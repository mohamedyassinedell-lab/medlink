from datetime import datetime, time
import pytz
from typing import Dict, Any

class StatusService:
    """Service to calculate doctor availability status"""
    
    @staticmethod
    def get_status(doctor):
        """Calculate current status for a doctor"""
        now = datetime.now(pytz.timezone('Africa/Algiers'))
        current_time = now.time()
        current_day = now.weekday()  # 0=Monday, 6=Sunday
        
        # Convert to Sunday-based (0=Sunday, 6=Saturday)
        current_day = (current_day + 1) % 7
        
        # Check for holidays
        today = now.date()
        for holiday in doctor.holidays:
            if holiday.start_date <= today <= holiday.end_date:
                return {
                    'status': 'ON_VACATION',
                    'label': '🏖️ في عطلة',
                    'color': 'orange',
                    'return_date': holiday.end_date,
                    'note': holiday.note_ar or holiday.note
                }
        
        # Get working hours for today
        working_hours = [wh for wh in doctor.working_hours 
                        if wh.day_of_week == current_day and not wh.is_closed]
        
        if not working_hours:
            return {
                'status': 'CLOSED',
                'label': '🔴 مغلق',
                'color': 'red',
                'message': 'العيادة مغلقة اليوم'
            }
        
        # Check if currently within working hours
        is_working = False
        for wh in working_hours:
            start = datetime.strptime(wh.start_time, '%H:%M').time()
            end = datetime.strptime(wh.end_time, '%H:%M').time()
            
            if start <= current_time <= end:
                is_working = True
                break
        
        if is_working:
            return {
                'status': 'AVAILABLE',
                'label': '🟢 متوفر الآن',
                'color': 'green',
                'message': 'العيادة مفتوحة الآن'
            }
        else:
            return {
                'status': 'CLOSED',
                'label': '🟠 مغلق الآن',
                'color': 'orange',
                'message': 'العيادة مغلقة الآن'
            }