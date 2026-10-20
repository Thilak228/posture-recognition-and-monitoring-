"""
SMTP Email System for AI Posture Monitor
Professional email notification system using direct SMTP delivery
Replaces Web3Forms with reliable Gmail/Outlook/Yahoo email service
"""

import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import logging

class SMTPEmailNotifier:
    """
    Professional SMTP Email Notification System
    Sends fall alerts, monitoring reports, and system notifications via SMTP
    """
    
    def __init__(self, config_file='email_config.json'):
        """
        Initialize SMTP email notifier
        
        Args:
            config_file: Path to email configuration file
        """
        self.config = self.load_config(config_file)
        self.smtp_config = self.config.get('smtp', {})
        self.email_settings = self.config.get('alert_settings', {})
        self.monitoring_settings = self.config.get('monitoring_settings', {})
        
        # Email templates and settings
        self.sender_name = self.config.get('sender_name', 'AI Posture Monitor - Elderly Care System')
        self.recipient_email = self.config.get('recipient_email', 'user@example.com')
        
        # Validate configuration
        if not self.smtp_config.get('smtp_username') or not self.smtp_config.get('smtp_password'):
            raise ValueError("SMTP credentials not configured. Run configure_gmail.py to set up email.")
    
    def load_config(self, config_file):
        """Load email configuration from JSON file"""
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            return config
        except Exception as e:
            raise ValueError(f"Failed to load email configuration: {e}")
    
    def send_fall_alert(self, fall_data):
        """
        Send urgent fall detection alert
        
        Args:
            fall_data: Dictionary containing fall detection information
                - subject_name: Name of the person
                - location: Location where fall occurred  
                - confidence: Detection confidence percentage
                - duration: Fall duration in seconds
                - state_sequence: State transition sequence
                - camera_source: Camera/source identifier
                - version: System version
        
        Returns:
            dict: Result with success status and message
        """
        try:
            subject = f"🚨 EMERGENCY FALL DETECTED – Immediate Attention Required"
            
            # Create comprehensive fall alert message with emergency keywords
            message_body = f"""🚨 EMERGENCY FALL DETECTION ALERT 🚨
URGENT: IMMEDIATE ATTENTION REQUIRED
EMERGENCY: FALL DETECTED
CRITICAL: MEDICAL EMERGENCY

Fall Details:
- Person: {fall_data.get('subject_name', 'Unknown')}
- Location: {fall_data.get('location', 'Unknown')}
- Detected: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- Confidence: {fall_data.get('confidence', 0)}%
- Fall Duration: {fall_data.get('duration', 0)} seconds
- State Sequence: {fall_data.get('state_sequence', 'Unknown')}

System Information:
- Camera Source: {fall_data.get('camera_source', 'Unknown')}
- System Version: {fall_data.get('version', '1.0.0')}

EMERGENCY ACTIONS REQUIRED IMMEDIATELY:
1. 🚨 CHECK ON {fall_data.get('subject_name', 'THE PERSON').upper()} IMMEDIATELY 🚨
2. ASSESS FOR INJURIES OR DISTRESS
3. CALL EMERGENCY SERVICES IF NEEDED (911)
4. CONTACT PRIMARY CAREGIVER OR FAMILY MEMBER
5. PROVIDE ASSISTANCE IF PERSON IS CONSCIOUS

⚠️ TIME-CRITICAL RESPONSE RECOMMENDED ⚠️
This is an AUTOMATED EMERGENCY ALERT from the AI Posture Monitor system.
URGENT MEDICAL ATTENTION MAY BE REQUIRED."""

            return self.send_email(subject, message_body, priority='critical')
            
        except Exception as e:
            return {'success': False, 'message': f'Fall alert error: {str(e)}'}
    
    def send_monitoring_report(self, report_data):
        """
        Send comprehensive monitoring report
        
        Args:
            report_data: Dictionary containing monitoring statistics
        
        Returns:
            dict: Result with success status and message
        """
        try:
            subject = f"📊 {report_data.get('period', 'Daily')} Monitoring Report - {report_data.get('subject_name', 'Unknown')}"
            
            # Create detailed monitoring report
            posture_stats = report_data.get('posture_statistics', {})
            
            message_body = f"""{report_data.get('period', 'DAILY').upper()} POSTURE MONITORING REPORT

Subject: {report_data.get('subject_name', 'Unknown')}
Report Period: {report_data.get('start_time', 'Unknown')} to {datetime.now().strftime('%Y-%m-%d %H:%M')}
Total Monitoring Time: {report_data.get('total_duration', 0)} minutes

POSTURE ANALYSIS:
- Standing Time: {posture_stats.get('standing_minutes', 0)} minutes ({posture_stats.get('standing_percentage', 0)}%)
- Walking Time: {posture_stats.get('walking_minutes', 0)} minutes ({posture_stats.get('walking_percentage', 0)}%)
- Sitting Time: {posture_stats.get('sitting_minutes', 0)} minutes ({posture_stats.get('sitting_percentage', 0)}%)
- Lying Down Time: {posture_stats.get('lying_minutes', 0)} minutes ({posture_stats.get('lying_percentage', 0)}%)
- Fall Incidents: {posture_stats.get('fall_minutes', 0)} minutes ({posture_stats.get('fall_percentage', 0)}%)
- Position Transitions: {posture_stats.get('transitions', 0)}
- Total Sedentary Time: {posture_stats.get('sedentary_minutes', 0)} minutes

HEALTH & ACTIVITY METRICS:
- Overall Activity Level: {report_data.get('activity_level', 'Unknown')}
- Mobility Score: {report_data.get('mobility_score', 'N/A')}/10
- Current Risk Assessment: {report_data.get('risk_assessment', 'Unknown')}

SAFETY & INCIDENTS:
- Fall Detection Events: {report_data.get('fall_count', 0)}
- Alert Notifications Sent: {report_data.get('alerts_sent', 0)}
- False Alarm Count: {report_data.get('false_alarms', 0)}
- System Detection Accuracy: {report_data.get('accuracy', 'N/A')}%

SYSTEM PERFORMANCE:
- System Uptime: {report_data.get('uptime', 'N/A')}%
- Data Quality Rating: {report_data.get('data_quality', 'Unknown')}
- Camera Feed Status: {report_data.get('camera_status', 'Unknown')}
- Last System Calibration: {report_data.get('last_calibration', 'N/A')}

Next automated report: {report_data.get('next_report', 'Tomorrow at same time')}

This automated report helps track daily activity patterns and health metrics.
For questions or concerns, please review the monitoring setup."""

            return self.send_email(subject, message_body, priority='normal')
            
        except Exception as e:
            return {'success': False, 'message': f'Monitoring report error: {str(e)}'}
    
    def send_system_alert(self, alert_type, alert_message, severity='normal'):
        """
        Send system alert notification
        
        Args:
            alert_type: Type of alert (e.g., 'Camera Error', 'System Startup')
            alert_message: Detailed alert message
            severity: Alert severity ('low', 'normal', 'high', 'critical')
        
        Returns:
            dict: Result with success status and message
        """
        try:
            # Map severity to email priority and emoji
            severity_map = {
                'low': {'priority': 'normal', 'emoji': '🔵', 'color': 'BLUE'},
                'normal': {'priority': 'normal', 'emoji': '🟡', 'color': 'YELLOW'}, 
                'high': {'priority': 'high', 'emoji': '🟠', 'color': 'ORANGE'},
                'critical': {'priority': 'critical', 'emoji': '🔴', 'color': 'RED'}
            }
            
            sev_info = severity_map.get(severity.lower(), severity_map['normal'])
            
            subject = f"{sev_info['emoji']} AI Posture Monitor - {alert_type}"
            
            message_body = f"""AI POSTURE MONITOR SYSTEM ALERT

Alert Type: {alert_type}
Severity: {severity.upper()}
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
System: {self.monitoring_settings.get('system_id', 'AI-Posture-Monitor-001')}

Issue Description:
{alert_message}

Technical Details:
- Error Code: N/A
- Affected Component: Unknown
- Impact Level: Monitoring may be affected

Recommended Actions:
- Check system status
- Review system logs
- Contact technical support if needed

System Status:
- Camera Feed: Unknown
- Processing: Unknown
- Data Storage: Unknown

This is an automated alert from the AI Posture Monitor system."""

            return self.send_email(subject, message_body, priority=sev_info['priority'])
            
        except Exception as e:
            return {'success': False, 'message': f'System alert error: {str(e)}'}
    
    def send_email(self, subject, message_body, priority='normal'):
        """
        Send email via SMTP
        
        Args:
            subject: Email subject line
            message_body: Email message content
            priority: Email priority ('normal', 'high', 'critical')
        
        Returns:
            dict: Result with success status and message
        """
        try:
            # Create email message
            msg = MIMEMultipart()
            msg['From'] = f"{self.sender_name} <{self.smtp_config['smtp_username']}>"
            msg['To'] = self.recipient_email
            msg['Subject'] = subject
            
            # Set priority headers for mobile notifications
            if priority in ['high', 'critical']:
                msg['X-Priority'] = '1' if priority == 'critical' else '2'
                msg['X-MSMail-Priority'] = 'High'
                msg['Importance'] = 'High'
                msg['X-Urgent'] = 'Yes'
                msg['X-Emergency'] = 'True'
                # Gmail specific headers for better mobile notifications
                msg['X-Gmail-Labels'] = 'Important,Urgent'
                msg['X-Android-Notification-Priority'] = 'high'
            
            # Create styled message body
            priority_colors = {
                'normal': '🔵',
                'high': '🟠', 
                'critical': '🔴'
            }
            
            priority_names = {
                'normal': 'NORMAL',
                'high': 'HIGH',
                'critical': 'CRITICAL'
            }
            
            formatted_message = f"""======================================================================
📧 EMAIL NOTIFICATION {priority_colors.get(priority, '🔵')}
======================================================================
From: {self.sender_name}
To: {self.recipient_email}
Subject: {subject}
Priority: {priority_names.get(priority, 'NORMAL')}
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
----------------------------------------------------------------------
Message Content:

{message_body}

======================================================================"""
            
            # Attach message body
            msg.attach(MIMEText(formatted_message, 'plain'))
            
            # Connect to SMTP server and send email
            with smtplib.SMTP(self.smtp_config['smtp_server'], self.smtp_config['smtp_port']) as server:
                if self.smtp_config.get('use_tls', True):
                    server.starttls()
                
                server.login(self.smtp_config['smtp_username'], self.smtp_config['smtp_password'])
                server.send_message(msg)
            
            # Print confirmation to console
            print(formatted_message)
            
            return {'success': True, 'message': 'Email sent successfully'}
            
        except Exception as e:
            error_msg = f"SMTP email error: {str(e)}"
            print(f"❌ {error_msg}")
            return {'success': False, 'message': error_msg}
    
    def test_connection(self):
        """
        Test SMTP connection and send test email
        
        Returns:
            dict: Test result with success status and message
        """
        try:
            test_subject = "🧪 AI Posture Monitor - Email System Test"
            test_message = f"""Email System Test Successful!

This is a test email from the AI Posture Monitor system.
If you receive this email, the SMTP configuration is working correctly.

Configuration Details:
- SMTP Server: {self.smtp_config['smtp_server']}
- SMTP Port: {self.smtp_config['smtp_port']}
- Username: {self.smtp_config['smtp_username']}
- TLS Enabled: {self.smtp_config.get('use_tls', True)}

Test performed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

The email notification system is ready for fall detection alerts!"""

            result = self.send_email(test_subject, test_message, priority='normal')
            
            if result['success']:
                return {'success': True, 'message': 'SMTP test email sent successfully!'}
            else:
                return {'success': False, 'message': f'SMTP test failed: {result["message"]}'}
                
        except Exception as e:
            return {'success': False, 'message': f'SMTP test error: {str(e)}'}

def main():
    """Test the SMTP email system"""
    print("🧪 Testing SMTP Email System...")
    
    try:
        notifier = SMTPEmailNotifier('email_config.json')
        result = notifier.test_connection()
        
        if result['success']:
            print("✅ SMTP Email System Test Passed!")
        else:
            print(f"❌ SMTP Email System Test Failed: {result['message']}")
    
    except Exception as e:
        print(f"❌ SMTP Email System Error: {e}")

if __name__ == "__main__":
    main()
