from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from sqlalchemy import func
from models import Leaves,Users

from routers.auth import get_current_user,db_dependency

router = APIRouter()


user_dependency=Annotated[dict,Depends(get_current_user)]

@router.get("/leaves/distribution")
def leave_distribution(
    db:db_dependency,
    current_user: user_dependency
):
    """
    Provides the count of leaves taken by leave type.
    """
    
    

    result = db.query(
    Leaves.leave_type,
    # func.count(Leaves.leave_type).label('leave_count'),
    func.sum(
        func.datediff(func.date(Leaves.end_date), func.date(Leaves.start_date)) + 1
        ).label('Total_Leave_Days')  # Add 1 to include both start and end dates
        ).filter(
        Leaves.user_id == current_user.id
        ).group_by(
        Leaves.leave_type
        ).all()

    if not result:
        raise HTTPException(status_code=404, detail="No leave data available")

    return {"distribution": result}


@router.get("/leaves/monthly-trends")
def monthly_trends(
    year: int,
    db: db_dependency,
    current_user: user_dependency
):
    # Use DATE_FORMAT for MySQL/MariaDB
    monthly_data = (
        db.query(
            func.date_format(Leaves.start_date, "%m").label("month"),
            # func.count(Leaves.id).label("leave_count"),
            func.sum(func.datediff(func.date(Leaves.end_date), func.date(Leaves.start_date))+1).label('Total_leaves_days')
            
        )
        .filter(func.date_format(Leaves.start_date, "%Y") == str(year),Leaves.user_id == current_user.id)
        .group_by("month")
        .order_by("month")
        .all()
    )
    return monthly_data
    # monthly_trends = {month: count for month, count in monthly_data}
    # return {"year": year, "monthly_trends": monthly_trends}


@router.get("/leaves/department-wise")
def department_wise_distribution(
    db:db_dependency,
    current_user: Users = Depends(get_current_user),
):
    """
    Returns the count of leaves taken by department.
    Requires a `department` field in the User model.
    """
    result = (
    db.query(
        Users.role.label("role"),
        Users.name.label("Name"),
        # func.count(Leaves.id).label("leave_count"),
        func.sum(func.datediff(Leaves.end_date, Leaves.start_date) + 1).label("total_leave_days")
    )
    .join(Leaves, Users.id == Leaves.user_id)
    .group_by(Users.role,Users.name)
    .having(func.sum(func.datediff(Leaves.end_date, Leaves.start_date) + 1) > 0)  # Example filter
    .all()
)

# Process the result
    output = [{"role": row.role,"Name":row.Name, "total_leave_days": row.total_leave_days} for row in result]

    if not result:
        raise HTTPException(status_code=200, detail="No department-wise leave data found")

    return result


