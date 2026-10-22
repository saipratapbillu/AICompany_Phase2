from sqlalchemy import text


class DashboardService:

    def get_summary(
        self,
        db
    ):

        return {

            "requirements":
                db.execute(
                    text(
                        '''
                        SELECT COUNT(*)
                        FROM Requirement
                        '''
                    )
                ).scalar(),

            "assessments":
                db.execute(
                    text(
                        '''
                        SELECT COUNT(*)
                        FROM RequirementAssessment
                        '''
                    )
                ).scalar(),

            "projects":
                db.execute(
                    text(
                        '''
                        SELECT COUNT(*)
                        FROM Project
                        '''
                    )
                ).scalar(),

            "users":
                db.execute(
                    text(
                        '''
                        SELECT COUNT(*)
                        FROM AppUser
                        '''
                    )
                ).scalar(),

            "approvals":
                db.execute(
                    text(
                        '''
                        SELECT COUNT(*)
                        FROM Approval
                        '''
                    )
                ).scalar()
        }