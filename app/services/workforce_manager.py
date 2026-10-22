class WorkforceManager:

    def assign_resources(
        self,
        project,
        required_skills
    ):

        assignments = []

        for skill in required_skills:

            assignments.append({

                "skill":
                    skill.skill_name,

                "resource":
                    f"AI Resource - {skill.skill_name}",

                "capacity":
                    100

            })

        return assignments

    def estimate_capacity(
        self,
        required_skills
    ):

        total = 0

        for skill in required_skills:

            if skill.estimated_effort_hours:

                total += (
                    skill.estimated_effort_hours
                )

        return total