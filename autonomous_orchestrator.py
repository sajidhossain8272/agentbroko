import time
import logging
import os
import sys
from master_state_machine import MasterStateMachine
from brain import Brain
from capabilities.capability_router import CapabilityRouter
from agent_supervisor import AgentSupervisor
from event_bus import EventBus
from goal_manager import GoalManager
from task_manager import TaskManager
from agent_memory import AgentMemory
from autonomous_scheduler import AutonomousScheduler

class AutonomousOrchestrator:
    def __init__(self):
        self.scheduler = AutonomousScheduler()
        self.sm = MasterStateMachine("STARTING")
        self.brain = Brain()
        self.router = CapabilityRouter()
        self.supervisor = AgentSupervisor()
        self.bus = EventBus()
        self.goal_mgr = GoalManager()
        self.task_mgr = TaskManager()
        self.memory = AgentMemory()
        self.last_business_cycle = 0.0

    def run_master_cycle(self):
        cycle_start = time.time()
        self.sm.transition_to("OBSERVING", "Cycle Wakeup")

        # 1. Observe & Update World Model
        self.supervisor.set_status("THINKING", task="Observing environment & world model", goal="Autonomous OS Operations")
        self.bus.emit("agent.decision.created", "Observing environment, checking goals & task queue...")

        # 2. Plan & Select Action
        self.sm.transition_to("PLANNING", "Evaluating Goal & Task Priorities")
        self.sm.transition_to("SELECTING", "Scoring Candidate Actions")
        action_decision = self.brain.evaluate_and_select_action()

        action_name = action_decision.get("action", "autonomous_master_execution")
        title = action_decision.get("title", "Master Autonomous Cycle")
        priority_score = action_decision.get("priority_score", 85.0)

        # 3. Execute Capability via Router
        self.sm.transition_to("EXECUTING", f"Invoking router for '{action_name}'")
        self.supervisor.set_status("EXECUTING", task=title)

        try:
            exec_result = self.router.route_and_execute(action_name, action_decision.get("payload"))
            
            # 4. Verify & Learn
            self.sm.transition_to("VERIFYING", "Validating capability outcome")
            status = exec_result.get("status") if isinstance(exec_result, dict) else "SUCCESS"
            
            self.sm.transition_to("LEARNING", "Updating memory & recording outcome")
            self.memory.record_event("episodic_memory", {
                "action": action_name,
                "title": title,
                "score": priority_score,
                "result": exec_result
            })

            if action_decision.get("task_id"):
                self.task_mgr.update_task_status(action_decision["task_id"], "COMPLETED", verification_result=str(status))

            self.sm.transition_to("WAITING", "Master Cycle Complete")
            self.supervisor.set_status("ONLINE", task="Unified Master OS Loop")
            
            duration = time.time() - cycle_start
            self.bus.emit("task.completed", f"Master Cycle Completed in {duration:.2f}s | Action: '{title}'", metadata={
                "duration_sec": round(duration, 2),
                "action": action_name,
                "result": exec_result
            })

            return exec_result

        except Exception as e:
            logging.error(f"[ORCHESTRATOR] Error during execution phase: {e}")
            self.sm.transition_to("RECOVERING", f"Execution error: {e}")
            self.sm.transition_to("WAITING", "Recovery complete")
            self.supervisor.set_status("ONLINE", task="Unified Master OS Loop")
            return {"status": "FAILED", "error": str(e)}

    def start_loop(self):
        print(f"🔒 [SINGLETON LOCK] Process lock acquired for PID: {self.scheduler.pid}")
        print("🚀 AgentBroko V8 Master Autonomous Orchestrator is ACTIVE...")
        self.sm.transition_to("WAITING", "Loop Initialized")

        # Explicit initialization of last_business_cycle
        self.last_business_cycle = time.time() - self.scheduler.BUSINESS_CYCLE + 5.0

        while True:
            try:
                now = time.time()

                # Check if 5-minute interval reached
                if now - self.last_business_cycle >= self.scheduler.BUSINESS_CYCLE:
                    self.run_master_cycle()
                    self.last_business_cycle = time.time()

                # Rapid monitor (every 60s)
                self.supervisor.emit_heartbeat()

            except KeyboardInterrupt:
                print("\n🛑 Shutting down AgentBroko V8 Orchestrator cleanly...")
                self.sm.transition_to("STOPPING", "KeyboardInterrupt")
                self.scheduler.release_lock()
                self.sm.transition_to("STOPPED", "Shutdown Complete")
                break
            except Exception as e:
                logging.error(f"Error in V8 Orchestrator loop: {e}")
                self.sm.transition_to("RECOVERING", f"Loop exception: {e}")
                self.sm.transition_to("WAITING", "Loop Recovered")

            time.sleep(self.scheduler.RAPID_MONITOR)
