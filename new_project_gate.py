import time
import logging
from event_bus import EventBus

class NewProjectGate:
    MIN_OPP_STRENGTH = 8.5
    MIN_EVIDENCE = 8.0
    MIN_EXPECTED_VAL = 500.0
    MIN_STRATEGIC_FIT = 8.0
    MAX_COST = 50.0
    MAX_RISK = 0.30

    def __init__(self):
        self.bus = EventBus()

    def evaluate_proposal(self, proposal):
        title = proposal.get("title", "Untitled Project")
        opp_strength = proposal.get("opp_strength", 5.0)
        evidence = proposal.get("evidence_score", 5.0)
        est_val = proposal.get("expected_value", 100.0)
        strat_fit = proposal.get("strategic_fit", 5.0)
        cost = proposal.get("cost", 100.0)
        risk = proposal.get("risk", 0.5)

        proposal_doc = {
            "title": title,
            "problem": proposal.get("problem", "Unspecified problem"),
            "evidence": proposal.get("evidence", "Weak or missing evidence"),
            "target_users": proposal.get("target_users", "Unspecified audience"),
            "potential_value": proposal.get("potential_value", 0.0),
            "expected_value": est_val,
            "cost": cost,
            "risk": risk,
            "why_now": proposal.get("why_now", "Idea generated"),
            "why_agentbroko": "Autonomous AI Agent OS ecosystem",
            "smallest_experiment": proposal.get("smallest_experiment", "Prototype validation"),
            "success_criteria": proposal.get("success_criteria", "User adoption"),
            "failure_criteria": proposal.get("failure_criteria", "Zero user engagement"),
            "evaluated_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        # Gate Evaluation
        reasons = []
        if opp_strength < self.MIN_OPP_STRENGTH: reasons.append(f"Opp Strength {opp_strength} < {self.MIN_OPP_STRENGTH}")
        if evidence < self.MIN_EVIDENCE: reasons.append(f"Evidence Score {evidence} < {self.MIN_EVIDENCE}")
        if est_val < self.MIN_EXPECTED_VAL: reasons.append(f"Expected Value ${est_val} < ${self.MIN_EXPECTED_VAL}")
        if strat_fit < self.MIN_STRATEGIC_FIT: reasons.append(f"Strategic Fit {strat_fit} < {self.MIN_STRATEGIC_FIT}")
        if cost > self.MAX_COST: reasons.append(f"Cost ${cost} > ${self.MAX_COST}")
        if risk > self.MAX_RISK: reasons.append(f"Risk {risk} > {self.MAX_RISK}")

        if reasons:
            proposal_doc["decision"] = "REJECTED"
            proposal_doc["rejection_reasons"] = reasons
            proposal_doc["advice"] = "Decision not strong enough. Improve AgentBroko core systems instead."
            self.bus.emit("project_gate.rejected", f"New Project Proposal '{title}' REJECTED by NewProjectGate", metadata=proposal_doc)
            return {"approved": False, "proposal_doc": proposal_doc}

        proposal_doc["decision"] = "APPROVED"
        self.bus.emit("project_gate.approved", f"New Project Proposal '{title}' APPROVED by NewProjectGate", metadata=proposal_doc)
        return {"approved": True, "proposal_doc": proposal_doc}
