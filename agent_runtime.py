import time
import logging
import os
import sys
from master_state_machine import MasterStateMachine
from executive_brain import ExecutiveBrain
from capabilities.capability_router import CapabilityRouter
from agent_supervisor import AgentSupervisor
from event_bus import EventBus
from goal_manager import GoalManager
from task_manager import TaskManager
from agent_memory import AgentMemory
from autonomous_scheduler import AutonomousScheduler

class AgentRuntime:
    def __init__(self):
        self.scheduler = AutonomousScheduler()
        self.sm = MasterStateMachine("STARTING")
        self.brain = ExecutiveBrain()
        self.router = CapabilityRouter()
        self.supervisor = AgentSupervisor()
        self.bus = EventBus()
        self.goal_mgr = GoalManager()
        self.task_mgr = TaskManager()
        self.memory = AgentMemory()

        # Explicit initialization of all scheduler timing variables.
        # This is deterministic and prevents a classic NameError/UnboundLocalError
        # path where a runtime loop expects a cycle marker that was never set.
        self.last_business_cycle = 0.0
        self.last_growth_cycle = 0.0
        self.last_moltbook_cycle = 0.0
        self.last_engineering_cycle = 0.0
        self.last_education_cycle = 0.0
        self.last_wallet_check = 0.0
        self.last_research_cycle = 0.0
        self.last_health_check = 0.0

    def _prime_runtime_timers(self):
        """Initialize deterministic scheduler markers once when the loop starts."""
        now = time.time()
        self.last_business_cycle = now - self.scheduler.BUSINESS_CYCLE + 5.0
        self.last_wallet_check = now
        self.last_research_cycle = now
        self.last_health_check = now
        self.last_growth_cycle = now
        self.last_moltbook_cycle = now
        self.last_engineering_cycle = now
        self.last_education_cycle = now
        return now

    def get_runtime_health(self):
        """Return a basic health structure for dashboard/observability."""
        return {
            "state": getattr(self.sm, "current_state", "UNKNOWN"),
            "last_business_cycle": self.last_business_cycle,
            "last_wallet_check": self.last_wallet_check,
            "last_health_check": getattr(self, "last_health_check", 0.0),
            "status": "ONLINE"
        }

    def run_master_cycle(self):
        cycle_start = time.time()
        self.sm.transition_to("OBSERVING", "Master Cycle Wakeup")

        # 1. Observe & Understand
        self.supervisor.set_status("THINKING", task="Observing environment & world model", goal="Autonomous OS Operations")
        self.bus.emit("agent.state.changed", "Observing environment, checking goals & task queue...")

        # 2. Discover, Score & Select
        self.sm.transition_to("PLANNING", "Evaluating Executive Priorities")
        self.sm.transition_to("SELECTING", "Scoring Candidate Actions via ExecutiveBrain")
        action_decision = self.brain.evaluate_world_and_select_action()

        action_name = action_decision.get("action", "autonomous_master_execution")
        title = action_decision.get("title", "Master Autonomous Cycle")
        priority_score = action_decision.get("priority_score", 85.0)

        # 3. Plan & Execute Capability via Router
        self.sm.transition_to("EXECUTING", f"Invoking router for '{action_name}'")
        self.supervisor.set_status("EXECUTING", task=title)

        try:
            exec_result = self.router.route_and_execute(action_name, action_decision)
            
            # 4. Measure & Learn
            self.sm.transition_to("VERIFYING", "Validating execution outcome")
            status = exec_result.get("status") if isinstance(exec_result, dict) else "SUCCESS"
            # Router default execution returns {"moltbook": ..., "business": ...} without a "status" key.
            # Treat any non-error result as SUCCESS.
            if status is None:
                status = "SUCCESS"
            
            # 4b. Complete claimed task if this decision came from the task queue
            task_id = action_decision.get("task_id")
            if task_id:
                self.task_mgr.update_task_status(
                    task_id,
                    "COMPLETED" if status == "SUCCESS" else "FAILED",
                    verification_result=f"Executed via {action_name} | Result: {status}"
                )
            
            self.sm.transition_to("LEARNING", "Updating memory & recording outcome")
            self.memory.record_event("episodic_memory", {
                "action": action_name,
                "title": title,
                "score": priority_score,
                "result": exec_result
            })

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
            logging.error(f"[RUNTIME] Error during execution phase: {e}")
            self.sm.transition_to("RECOVERING", f"Execution error: {e}")
            self.sm.transition_to("WAITING", "Recovery complete")
            self.supervisor.set_status("ONLINE", task="Unified Master OS Loop")
            return {"status": "FAILED", "error": str(e)}

    def start_loop(self):
        print(f"🔒 [SINGLETON LOCK] Process lock acquired for PID: {self.scheduler.pid}")
        print("🚀 AgentBroko V9 Master AgentRuntime is ACTIVE...")
        self.sm.transition_to("WAITING", "Loop Initialized")

        # Explicit initialization of timing markers right before loop.
        self._prime_runtime_timers()

        while True:
            try:
                now = time.time()

                # Check evaluation heartbeat (every 5 minutes)
                if now - self.last_business_cycle >= self.scheduler.BUSINESS_CYCLE:
                    self.run_master_cycle()
                    self.last_business_cycle = time.time()
                    self.scheduler.update_heartbeat("master_cycle")
                    # Flush all log handlers so the log file is always current on disk
                    for handler in logging.getLogger().handlers:
                        try:
                            handler.flush()
                        except Exception:
                            pass

                # Rapid monitor heartbeat (every 60s)
                self.supervisor.emit_heartbeat()

            except KeyboardInterrupt:
                print("\n🛑 Shutting down AgentBroko V9 Runtime cleanly...")
                self.sm.transition_to("STOPPING", "KeyboardInterrupt")
                self.scheduler.release_lock()
                self.sm.transition_to("STOPPED", "Shutdown Complete")
                break
            except Exception as e:
                logging.error(f"Error in V9 Runtime loop: {e}")
                self.sm.transition_to("RECOVERING", f"Loop exception: {e}")
                self.sm.transition_to("WAITING", "Loop Recovered")

            time.sleep(self.scheduler.RAPID_MONITOR)


class UnifiedAgentRuntime(AgentRuntime):
    """Compatibility alias for the unified runtime surface.

    The production runtime is already implemented through AgentRuntime, but this
    name is part of the operating system contract the repository is asked to
    support. Keeping a concrete class here avoids accidental duplication or
    divergent runtime loops.
    """

    pass
