import uuid

from datetime import datetime, timezone

from app.models.entities import (
    Project
)


class ProjectFactory:

    def create_project(
        self,
        db,
        requirement
    ):

        project = Project(
            ProjectID=uuid.uuid4(),
            RequirementID=requirement.RequirementID,
            ProjectName=requirement.Title,
            Status="Planned",
            CreatedAtUtc=datetime.now(
                timezone.utc
            )
        )

        db.add(project)

        db.commit()

        db.refresh(project)

        return project

    def generate_default_tasks(
        self,
        project_id
    ):

        return [

            "Requirements Gathering",

            "Solution Design",

            "Development",

            "Testing",

            "Deployment",

            "Training",

            "Hypercare"

        ]