const token =
localStorage.getItem("token");

if(!token){

    window.location="/login";
}

async function loadProfile(){

    try{

        const payload =
        JSON.parse(
            atob(
                token.split(".")[1]
            )
        );

        document.getElementById(
            "userName"
        ).innerText =
        payload.name;

        document.getElementById(
            "roleBadge"
        ).innerText =
        payload.role;

    }
    catch(e){

        logout();
    }
}

async function loadDashboard(){

    try{

        const response =
        await fetch(
            "/dashboard/api",
            {
                headers:{
                    Authorization:
                    `Bearer ${token}`
                }
            }
        );

        if(response.ok){

            const data =
            await response.json();

            document.getElementById(
                "requirementsCount"
            ).innerText =
            data.requirements || 0;

            document.getElementById(
                "assessmentsCount"
            ).innerText =
            data.assessments || 0;

            document.getElementById(
                "projectsCount"
            ).innerText =
            data.projects || 0;

            document.getElementById(
                "approvalsCount"
            ).innerText =
            data.approvals || 0;
        }

    }catch(e){

        console.error(e);
    }
}

function logout(){

    localStorage.removeItem(
        "token"
    );

    localStorage.removeItem(
        "user"
    );

    window.location="/login";
}

loadProfile();
loadDashboard();