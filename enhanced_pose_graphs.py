"""
Enhanced Pose Estimation Graphing Module
Creates comprehensive visualizations of pose detection data with robust error handling
"""
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend to avoid display issues
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
try:
    import seaborn as sns
except ImportError:
    print("⚠️ Seaborn not available, using basic styling")
    sns = None
from collections import Counter
import os

class EnhancedPoseGraphGenerator:
    def __init__(self):
        """Initialize the graph generator with styling"""
        try:
            # Try to use seaborn style, fallback to default if not available
            try:
                plt.style.use('seaborn-v0_8')
            except:
                try:
                    plt.style.use('seaborn')
                except:
                    plt.style.use('default')
            
            # Set color palette
            try:
                if sns is not None:
                    sns.set_palette("husl")
            except:
                pass  # Continue with default colors if seaborn fails
                
        except Exception as e:
            print(f"⚠️ Warning: Some styling features unavailable: {e}")
        
        self.colors = {
            'standing': '#2E86AB',  # Blue
            'sitting': '#A23B72',   # Purple
            'lying': '#F18F01',     # Orange
            'walking': '#00A300',   # Green
            'fall': '#DC143C',      # Crimson Red (emergency color)
            'unknown': '#C73E1D'    # Red
        }
        self.pose_emojis = {
            'standing': '🧍',
            'sitting': '💺', 
            'lying': '🛏️',
            'walking': '🚶',
            'fall': '🚨',           # Emergency/alert emoji
            'unknown': '❓'
        }
        
    def create_comprehensive_report(self, pose_history, pose_stats, session_info, output_dir="pose_graphs"):
        """Create a comprehensive set of graphs and save them"""
        try:
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                
            print("📊 Generating comprehensive pose analysis graphs...")
            
            # Convert pose history to DataFrame for easier plotting
            if pose_history:
                df = pd.DataFrame(pose_history)
                df['timestamp'] = pd.to_datetime(df['timestamp'])
            else:
                print("⚠️ No pose history data available")
                return []
            
            generated_files = []
            
            # 1. Real-time pose timeline
            timeline_file = self.create_pose_timeline(df, session_info, output_dir)
            if timeline_file:
                generated_files.append(timeline_file)
            
            # 2. Pose distribution pie chart
            pie_file = self.create_pose_distribution_pie(pose_stats, session_info, output_dir)
            if pie_file:
                generated_files.append(pie_file)
            
            # 3. Confidence levels over time
            confidence_file = self.create_confidence_timeline(df, session_info, output_dir)
            if confidence_file:
                generated_files.append(confidence_file)
            
            # 4. Activity patterns heatmap
            heatmap_file = self.create_activity_heatmap(df, session_info, output_dir)
            if heatmap_file:
                generated_files.append(heatmap_file)
            
            # 5. Pose transition analysis
            transition_file = self.create_transition_analysis(df, session_info, output_dir)
            if transition_file:
                generated_files.append(transition_file)
            
            # 6. Comprehensive dashboard
            dashboard_file = self.create_dashboard(df, pose_stats, session_info, output_dir)
            if dashboard_file:
                generated_files.append(dashboard_file)
            
            print(f"✅ Generated {len(generated_files)} visualization files")
            return generated_files
            
        except Exception as e:
            print(f"❌ Error in comprehensive report generation: {e}")
            return []
        if timeline_file:
            generated_files.append(timeline_file)
        
        # 2. Pose distribution pie chart
        pie_file = self.create_pose_distribution_pie(pose_stats, session_info, output_dir)
        if pie_file:
            generated_files.append(pie_file)
        
        # 3. Confidence levels over time
        confidence_file = self.create_confidence_timeline(df, session_info, output_dir)
        if confidence_file:
            generated_files.append(confidence_file)
        
        # 4. Activity patterns heatmap
        heatmap_file = self.create_activity_heatmap(df, session_info, output_dir)
        if heatmap_file:
            generated_files.append(heatmap_file)
        
        # 5. Pose transition analysis
        transition_file = self.create_transition_analysis(df, session_info, output_dir)
        if transition_file:
            generated_files.append(transition_file)
        
        # 6. Comprehensive dashboard
        dashboard_file = self.create_dashboard(df, pose_stats, session_info, output_dir)
        if dashboard_file:
            generated_files.append(dashboard_file)
        
        print(f"✅ Generated {len(generated_files)} visualization files")
        return generated_files
    
    def create_pose_timeline(self, df, session_info, output_dir):
        """Create a timeline showing pose changes over time"""
        try:
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
            
            # Convert poses to numeric for plotting
            pose_mapping = {'standing': 5, 'walking': 4, 'sitting': 3, 'lying': 2, 'fall': 1, 'unknown': 0}
            df['pose_numeric'] = df['pose'].map(pose_mapping)
            
            # Timeline plot
            for pose in df['pose'].unique():
                pose_data = df[df['pose'] == pose]
                ax1.scatter(pose_data['timestamp'], pose_data['pose_numeric'], 
                           c=self.colors[pose], label=f"{self.pose_emojis[pose]} {pose.title()}", 
                           s=50, alpha=0.7)
            
            ax1.set_ylabel('Pose Type')
            ax1.set_title(f'🕐 Real-time Pose Detection Timeline\nSession: {session_info["start_time"]} - Duration: {session_info["duration"]:.1f} min', 
                         fontsize=14, fontweight='bold')
            ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            ax1.grid(True, alpha=0.3)
            ax1.set_yticks([0, 1, 2, 3, 4, 5])
            ax1.set_yticklabels(['Unknown', 'Fall', 'Lying', 'Sitting', 'Walking', 'Standing'])
            
            # Pose duration bars
            pose_counts = df['pose'].value_counts()
            total_time = session_info["duration"]
            
            poses = list(pose_counts.index)
            durations = [(count / len(df)) * total_time for count in pose_counts.values]
            colors = [self.colors[pose] for pose in poses]
            
            bars = ax2.bar(poses, durations, color=colors, alpha=0.8)
            ax2.set_ylabel('Duration (minutes)')
            ax2.set_title('📊 Time Spent in Each Pose', fontsize=12, fontweight='bold')
            ax2.grid(True, alpha=0.3)
            
            # Add value labels on bars
            for bar, duration in zip(bars, durations):
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                        f'{duration:.1f}m', ha='center', va='bottom', fontweight='bold')
            
            plt.tight_layout()
            filename = f"{output_dir}/pose_timeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close()
            print(f"✅ Timeline graph saved: {filename}")
            return filename
            
        except Exception as e:
            print(f"❌ Error creating timeline: {e}")
            return None
    
    def create_pose_distribution_pie(self, pose_stats, session_info, output_dir):
        """Create pie chart showing pose distribution"""
        try:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
            
            # Count-based pie chart
            counts = [stats['count'] for stats in pose_stats.values()]
            labels = [f"{self.pose_emojis[pose]} {pose.title()}\n({count} frames)" 
                     for pose, count in zip(pose_stats.keys(), counts)]
            colors = [self.colors[pose] for pose in pose_stats.keys()]
            
            wedges1, texts1, autotexts1 = ax1.pie(counts, labels=labels, colors=colors, autopct='%1.1f%%', 
                                                  startangle=90, textprops={'fontsize': 10})
            ax1.set_title(f'📊 Pose Distribution by Frame Count\nTotal Frames: {sum(counts)}', 
                         fontsize=14, fontweight='bold')
            
            # Time-based pie chart
            total_time = session_info["duration"]
            times = [(count / sum(counts)) * total_time for count in counts]
            labels_time = [f"{self.pose_emojis[pose]} {pose.title()}\n({time:.1f} min)" 
                          for pose, time in zip(pose_stats.keys(), times)]
            
            wedges2, texts2, autotexts2 = ax2.pie(times, labels=labels_time, colors=colors, autopct='%1.1f%%', 
                                                  startangle=90, textprops={'fontsize': 10})
            ax2.set_title(f'⏱️ Pose Distribution by Time\nTotal Time: {total_time:.1f} minutes', 
                         fontsize=14, fontweight='bold')
            
            plt.tight_layout()
            filename = f"{output_dir}/pose_distribution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close()
            print(f"✅ Distribution pie chart saved: {filename}")
            return filename
            
        except Exception as e:
            print(f"❌ Error creating pie chart: {e}")
            return None
    
    def create_confidence_timeline(self, df, session_info, output_dir):
        """Create confidence levels timeline"""
        try:
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
            
            # Confidence over time
            ax1.plot(df['timestamp'], df['confidence'], color='#2E86AB', linewidth=2, alpha=0.8)
            ax1.fill_between(df['timestamp'], df['confidence'], alpha=0.3, color='#2E86AB')
            ax1.set_ylabel('Confidence Score')
            ax1.set_title(f'🎯 Detection Confidence Over Time\nAverage: {df["confidence"].mean():.2f}', 
                         fontsize=14, fontweight='bold')
            ax1.grid(True, alpha=0.3)
            ax1.set_ylim(0, 1)
            
            # Confidence by pose type
            confidence_by_pose = df.groupby('pose')['confidence'].agg(['mean', 'std', 'count'])
            poses = confidence_by_pose.index
            means = confidence_by_pose['mean']
            stds = confidence_by_pose['std']
            colors = [self.colors[pose] for pose in poses]
            
            bars = ax2.bar(poses, means, yerr=stds, color=colors, alpha=0.8, capsize=5)
            ax2.set_ylabel('Average Confidence')
            ax2.set_title('📈 Confidence Levels by Pose Type', fontsize=12, fontweight='bold')
            ax2.grid(True, alpha=0.3)
            
            # Add value labels
            for bar, mean in zip(bars, means):
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                        f'{mean:.2f}', ha='center', va='bottom', fontweight='bold')
            
            plt.tight_layout()
            filename = f"{output_dir}/confidence_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close()
            print(f"✅ Confidence analysis saved: {filename}")
            return filename
            
        except Exception as e:
            print(f"❌ Error creating confidence timeline: {e}")
            return None
    
    def create_activity_heatmap(self, df, session_info, output_dir):
        """Create activity pattern heatmap"""
        try:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
            
            # Create time bins (every 10 seconds for short sessions)
            df['time_bin'] = pd.cut(df['timestamp'], bins=min(20, len(df)//5))
            
            # Activity intensity heatmap
            activity_matrix = df.groupby(['time_bin', 'pose']).size().unstack(fill_value=0)
            
            if not activity_matrix.empty:
                try:
                    if sns is not None:
                        sns.heatmap(activity_matrix.T, annot=True, fmt='d', cmap='YlOrRd', 
                                   ax=ax1, cbar_kws={'label': 'Frame Count'})
                    else:
                        # Fallback if seaborn fails
                        im = ax1.imshow(activity_matrix.T.values, cmap='YlOrRd', aspect='auto')
                        plt.colorbar(im, ax=ax1, label='Frame Count')
                except:
                    # Fallback if seaborn fails
                    im = ax1.imshow(activity_matrix.T.values, cmap='YlOrRd', aspect='auto')
                    plt.colorbar(im, ax=ax1, label='Frame Count')
                    
                ax1.set_title('🔥 Activity Intensity Heatmap', fontsize=14, fontweight='bold')
                ax1.set_xlabel('Time Periods')
                ax1.set_ylabel('Pose Types')
            else:
                ax1.text(0.5, 0.5, 'Insufficient data for heatmap', ha='center', va='center', transform=ax1.transAxes)
            
            # Pose transition matrix
            df_sorted = df.sort_values('timestamp')
            transitions = []
            for i in range(1, len(df_sorted)):
                prev_pose = df_sorted.iloc[i-1]['pose']
                curr_pose = df_sorted.iloc[i]['pose']
                if prev_pose != curr_pose:
                    transitions.append((prev_pose, curr_pose))
            
            if transitions:
                transition_matrix = pd.DataFrame(index=df['pose'].unique(), columns=df['pose'].unique())
                transition_matrix = transition_matrix.fillna(0)
                
                for prev, curr in transitions:
                    transition_matrix.loc[prev, curr] += 1
                
                try:
                    if sns is not None:
                        sns.heatmap(transition_matrix.astype(int), annot=True, fmt='d', cmap='Blues',
                                   ax=ax2, cbar_kws={'label': 'Transition Count'})
                    else:
                        # Fallback if seaborn fails
                        im = ax2.imshow(transition_matrix.astype(int).values, cmap='Blues', aspect='auto')
                        plt.colorbar(im, ax=ax2, label='Transition Count')
                except:
                    # Fallback if seaborn fails
                    im = ax2.imshow(transition_matrix.astype(int).values, cmap='Blues', aspect='auto')
                    plt.colorbar(im, ax=ax2, label='Transition Count')
                    
                ax2.set_title('🔄 Pose Transition Matrix', fontsize=14, fontweight='bold')
                ax2.set_xlabel('To Pose')
                ax2.set_ylabel('From Pose')
            else:
                ax2.text(0.5, 0.5, 'No transitions detected', ha='center', va='center', transform=ax2.transAxes)
            
            plt.tight_layout()
            filename = f"{output_dir}/activity_heatmap_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close()
            print(f"✅ Activity heatmap saved: {filename}")
            return filename
            
        except Exception as e:
            print(f"❌ Error creating heatmap: {e}")
            return None
    
    def create_transition_analysis(self, df, session_info, output_dir):
        """Analyze and visualize pose transitions"""
        try:
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
            
            # Calculate transitions
            df_sorted = df.sort_values('timestamp')
            transitions = []
            transition_times = []
            
            for i in range(1, len(df_sorted)):
                prev_pose = df_sorted.iloc[i-1]['pose']
                curr_pose = df_sorted.iloc[i]['pose']
                if prev_pose != curr_pose:
                    transitions.append(f"{prev_pose} → {curr_pose}")
                    transition_times.append(df_sorted.iloc[i]['timestamp'])
            
            # Transition frequency
            if transitions:
                transition_counts = Counter(transitions)
                trans_labels = list(transition_counts.keys())
                trans_values = list(transition_counts.values())
                
                ax1.barh(trans_labels, trans_values, color='skyblue', alpha=0.8)
                ax1.set_xlabel('Frequency')
                ax1.set_title('🔄 Pose Transition Frequency', fontsize=12, fontweight='bold')
                ax1.grid(True, alpha=0.3)
            
            # Pose stability (how long poses are maintained)
            pose_durations = []
            current_pose = df_sorted.iloc[0]['pose']
            current_start = df_sorted.iloc[0]['timestamp']
            
            for i in range(1, len(df_sorted)):
                if df_sorted.iloc[i]['pose'] != current_pose:
                    duration = (df_sorted.iloc[i]['timestamp'] - current_start).total_seconds()
                    pose_durations.append({'pose': current_pose, 'duration': duration})
                    current_pose = df_sorted.iloc[i]['pose']
                    current_start = df_sorted.iloc[i]['timestamp']
            
            # Add final pose duration
            final_duration = (df_sorted.iloc[-1]['timestamp'] - current_start).total_seconds()
            pose_durations.append({'pose': current_pose, 'duration': final_duration})
            
            if pose_durations:
                duration_df = pd.DataFrame(pose_durations)
                duration_by_pose = duration_df.groupby('pose')['duration'].agg(['mean', 'std', 'count'])
                
                poses = duration_by_pose.index
                means = duration_by_pose['mean']
                stds = duration_by_pose['std']
                colors = [self.colors[pose] for pose in poses]
                
                bars = ax2.bar(poses, means, yerr=stds, color=colors, alpha=0.8, capsize=5)
                ax2.set_ylabel('Duration (seconds)')
                ax2.set_title('⏱️ Average Pose Stability', fontsize=12, fontweight='bold')
                ax2.grid(True, alpha=0.3)
                
                for bar, mean in zip(bars, means):
                    height = bar.get_height()
                    ax2.text(bar.get_x() + bar.get_width()/2., height + 1,
                            f'{mean:.1f}s', ha='center', va='bottom', fontweight='bold')
            
            # Transition timeline
            if transition_times:
                ax3.scatter(transition_times, range(len(transition_times)), 
                           c='red', s=100, alpha=0.7, marker='x')
                ax3.set_xlabel('Time')
                ax3.set_ylabel('Transition Number')
                ax3.set_title('📍 Transition Timeline', fontsize=12, fontweight='bold')
                ax3.grid(True, alpha=0.3)
            
            # Activity summary
            total_frames = len(df)
            total_transitions = len(transitions)
            avg_confidence = df['confidence'].mean()
            
            summary_text = f"""
            📊 SESSION SUMMARY
            
            Total Frames: {total_frames}
            Total Transitions: {total_transitions}
            Transition Rate: {total_transitions/session_info['duration']:.1f}/min
            Average Confidence: {avg_confidence:.2f}
            Most Stable Pose: {df['pose'].mode()[0] if not df.empty else 'N/A'}
            """
            
            ax4.text(0.1, 0.5, summary_text, transform=ax4.transAxes, fontsize=11,
                    verticalalignment='center', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
            ax4.set_xlim(0, 1)
            ax4.set_ylim(0, 1)
            ax4.axis('off')
            ax4.set_title('📋 Analysis Summary', fontsize=12, fontweight='bold')
            
            plt.tight_layout()
            filename = f"{output_dir}/transition_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close()
            print(f"✅ Transition analysis saved: {filename}")
            return filename
            
        except Exception as e:
            print(f"❌ Error creating transition analysis: {e}")
            return None
    
    def create_dashboard(self, df, pose_stats, session_info, output_dir):
        """Create comprehensive dashboard"""
        try:
            fig = plt.figure(figsize=(20, 12))
            gs = fig.add_gridspec(3, 4, hspace=0.3, wspace=0.3)
            
            # Main title
            fig.suptitle(f'🏥 Enhanced AI Posture Monitoring Dashboard\nSession: {session_info["start_time"]} | Duration: {session_info["duration"]:.1f} minutes', 
                        fontsize=18, fontweight='bold')
            
            # 1. Pose timeline (large)
            ax1 = fig.add_subplot(gs[0, :2])
            pose_mapping = {'standing': 5, 'walking': 4, 'sitting': 3, 'lying': 2, 'fall': 1, 'unknown': 0}
            df['pose_numeric'] = df['pose'].map(pose_mapping)
            
            for pose in df['pose'].unique():
                pose_data = df[df['pose'] == pose]
                ax1.scatter(pose_data['timestamp'], pose_data['pose_numeric'], 
                           c=self.colors[pose], label=f"{self.pose_emojis[pose]} {pose.title()}", 
                           s=30, alpha=0.7)
            
            ax1.set_ylabel('Pose')
            ax1.set_title('🕐 Real-time Timeline', fontweight='bold')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            ax1.set_yticks([0, 1, 2, 3, 4, 5])
            ax1.set_yticklabels(['Unknown', 'Fall', 'Lying', 'Sitting', 'Walking', 'Standing'])
            
            # 2. Distribution pie
            ax2 = fig.add_subplot(gs[0, 2:])
            counts = [stats['count'] for stats in pose_stats.values()]
            labels = [f"{self.pose_emojis[pose]} {pose.title()}" for pose in pose_stats.keys()]
            colors = [self.colors[pose] for pose in pose_stats.keys()]
            
            ax2.pie(counts, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            ax2.set_title('📊 Pose Distribution', fontweight='bold')
            
            # 3. Confidence timeline
            ax3 = fig.add_subplot(gs[1, :2])
            ax3.plot(df['timestamp'], df['confidence'], color='#2E86AB', linewidth=2)
            ax3.fill_between(df['timestamp'], df['confidence'], alpha=0.3, color='#2E86AB')
            ax3.set_ylabel('Confidence')
            ax3.set_title(f'🎯 Detection Confidence (Avg: {df["confidence"].mean():.2f})', fontweight='bold')
            ax3.grid(True, alpha=0.3)
            
            # 4. Statistics table
            ax4 = fig.add_subplot(gs[1, 2:])
            ax4.axis('off')
            
            # Create statistics table
            total_frames = sum(stats['count'] for stats in pose_stats.values())
            table_data = []
            for pose, stats in pose_stats.items():
                count = stats['count']
                percentage = (count / total_frames * 100) if total_frames > 0 else 0
                time_minutes = (count / total_frames * session_info['duration']) if total_frames > 0 else 0
                table_data.append([
                    f"{self.pose_emojis[pose]} {pose.title()}", 
                    f"{count}", 
                    f"{percentage:.1f}%", 
                    f"{time_minutes:.1f}m"
                ])
            
            table = ax4.table(cellText=table_data,
                            colLabels=['Pose', 'Frames', 'Percentage', 'Time'],
                            cellLoc='center',
                            loc='center')
            table.auto_set_font_size(False)
            table.set_fontsize(10)
            table.scale(1, 2)
            ax4.set_title('📈 Detailed Statistics', fontweight='bold')
            
            # 5. Activity bars
            ax5 = fig.add_subplot(gs[2, :2])
            pose_counts = df['pose'].value_counts()
            poses = list(pose_counts.index)
            counts = list(pose_counts.values)
            colors = [self.colors[pose] for pose in poses]
            
            bars = ax5.bar(poses, counts, color=colors, alpha=0.8)
            ax5.set_ylabel('Frame Count')
            ax5.set_title('📊 Activity Summary', fontweight='bold')
            ax5.grid(True, alpha=0.3)
            
            for bar, count in zip(bars, counts):
                height = bar.get_height()
                ax5.text(bar.get_x() + bar.get_width()/2., height + 1,
                        f'{count}', ha='center', va='bottom', fontweight='bold')
            
            # 6. Health metrics
            ax6 = fig.add_subplot(gs[2, 2:])
            ax6.axis('off')
            
            # Calculate health metrics
            standing_time = (pose_stats.get('standing', {}).get('count', 0) / total_frames * session_info['duration']) if total_frames > 0 else 0
            walking_time = (pose_stats.get('walking', {}).get('count', 0) / total_frames * session_info['duration']) if total_frames > 0 else 0
            sitting_time = (pose_stats.get('sitting', {}).get('count', 0) / total_frames * session_info['duration']) if total_frames > 0 else 0
            lying_time = (pose_stats.get('lying', {}).get('count', 0) / total_frames * session_info['duration']) if total_frames > 0 else 0
            fall_time = (pose_stats.get('fall', {}).get('count', 0) / total_frames * session_info['duration']) if total_frames > 0 else 0
            
            active_time = standing_time + walking_time
            sedentary_time = sitting_time + lying_time
            activity_ratio = active_time / (active_time + sedentary_time) if (active_time + sedentary_time) > 0 else 0
            
            # Fall alerts section
            fall_count = pose_stats.get('fall', {}).get('count', 0)
            fall_status = "🚨 CRITICAL" if fall_count > 0 else "✅ SAFE"
            
            health_text = f"""
            🏥 HEALTH METRICS
            
            Active Time: {active_time:.1f} min ({(active_time/session_info['duration']*100):.1f}%)
            ├─ Standing: {standing_time:.1f} min
            ├─ Walking: {walking_time:.1f} min  
            Sedentary Time: {sedentary_time:.1f} min ({(sedentary_time/session_info['duration']*100):.1f}%)
            Activity Ratio: {activity_ratio:.2f}
            
            🚨 SAFETY STATUS: {fall_status}
            Fall Incidents: {fall_count} ({fall_time:.1f} min)
            
            📊 SESSION QUALITY
            Average Confidence: {df['confidence'].mean():.2f}
            Total Transitions: {len(set(df.index[df['pose'] != df['pose'].shift()]))}
            Detection Quality: {'Excellent' if df['confidence'].mean() > 0.8 else 'Good' if df['confidence'].mean() > 0.6 else 'Fair'}
            """
            
            ax6.text(0.05, 0.5, health_text, transform=ax6.transAxes, fontsize=11,
                    verticalalignment='center', 
                    bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
            ax6.set_title('💚 Health Assessment', fontweight='bold')
            
            filename = f"{output_dir}/comprehensive_dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close()
            print(f"✅ Comprehensive dashboard saved: {filename}")
            return filename
            
        except Exception as e:
            print(f"❌ Error creating dashboard: {e}")
            return None

def test_graph_generation():
    """Test the graph generation with sample data"""
    print("🧪 Testing Enhanced Pose Graph Generation...")
    
    # Sample data for testing
    sample_history = []
    base_time = datetime.now() - timedelta(minutes=2)
    
    # Generate sample pose sequence
    poses = ['standing'] * 20 + ['sitting'] * 15 + ['standing'] * 10 + ['sitting'] * 8 + ['lying'] * 5
    
    for i, pose in enumerate(poses):
        sample_history.append({
            'timestamp': base_time + timedelta(seconds=i*2),
            'pose': pose,
            'confidence': np.random.uniform(0.6, 0.9)
        })
    
    sample_stats = {
        'standing': {'count': 30, 'confidence_scores': [0.8] * 30},
        'sitting': {'count': 23, 'confidence_scores': [0.7] * 23},
        'lying': {'count': 5, 'confidence_scores': [0.9] * 5},
        'unknown': {'count': 0, 'confidence_scores': []}
    }
    
    sample_session = {
        'start_time': base_time.strftime('%Y-%m-%d %H:%M:%S'),
        'duration': 2.0
    }
    
    # Generate graphs
    grapher = EnhancedPoseGraphGenerator()
    files = grapher.create_comprehensive_report(sample_history, sample_stats, sample_session)
    
    print(f"✅ Generated {len(files)} test graph files")
    return files

if __name__ == "__main__":
    test_graph_generation()
