import streamlit as st

# --- 1. APP CONFIGURATION ---
st.set_page_config(page_title="Candy & Coco's Hub", page_icon="👑", layout="centered")

# --- 2. INITIALIZE DATABASE (SHARED SESSION STATE) ---
if "tasks" not in st.session_state:
    st.session_state.tasks = [
        {"id": 1, "title": "Complete Class 12 Chemistry revision chapter", "points": 100, "status": "Pending"},
        {"id": 2, "title": "Organize study desk", "points": 30, "status": "Completed"}
    ]

if "rewards" not in st.session_state:
    st.session_state.rewards = [
        {"id": 1, "title": "Ice Cream Cheat Day", "cost": 150, "claimed": False},
        {"id": 2, "title": "Weekend Movie Night Picker", "cost": 200, "claimed": False}
    ]

if "coco_points" not in st.session_state:
    st.session_state.coco_points = 100  # Starting balance

if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

# --- 3. AUTHENTICATION ---
def login(username, password):
    if username.lower() == "candy" and password == "candy123":  # Replace with Candy's password
        st.session_state.logged_in_user = "Candy"
        st.rerun()
    elif username.lower() == "coco" and password == "queen coco":
        st.session_state.logged_in_user = "Coco"
        st.rerun()
    else:
        st.error("❌ Incorrect username or password.")

# --- LOGIN SCREEN ---
if st.session_state.logged_in_user is None:
    st.title("👑 The Shared Quest Hub")
    st.subheader("Please sign in to view the dashboard")
    
    user_input = st.text_input("Username")
    pass_input = st.text_input("Password", type="password")
    
    if st.button("Log In", use_container_width=True):
        if user_input and pass_input:
            login(user_input, pass_input)
        else:
            st.warning("Please fill in both fields.")
    st.stop()

# --- 4. MAIN SHARED DASHBOARD ---
current_user = st.session_state.logged_in_user

# Header Section
st.title("✨ Our Shared Dashboard")
col_user, col_logout = st.columns([3, 1])
col_user.write(f"Logged in as: **{current_user}** 👤")
if col_logout.button("Log Out", size="small"):
    st.session_state.logged_in_user = None
    st.rerun()

st.markdown("---")

# Shared Scoreboard
st.metric(label="🪙 Coco's Total Points Balance", value=f"{st.session_state.coco_points} pts")

st.markdown("---")

# --- 5. TASKS SECTION ---
st.header("📋 Quests & Tasks")

# CANDY ONLY: Create Tasks
if current_user == "Candy":
    with st.expander("➕ Add a New Task (Candy Only)", expanded=False):
        new_task_title = st.text_input("What is the task?")
        new_task_pts = st.number_input("Points Reward", min_value=5, max_value=500, step=5, value=50)
        if st.button("Deploy Task to Board"):
            if new_task_title:
                new_id = len(st.session_state.tasks) + 1
                st.session_state.tasks.append({
                    "id": new_id,
                    "title": new_task_title,
                    "points": new_task_pts,
                    "status": "Pending"
                })
                st.success(f"Added: {new_task_title}")
                st.rerun()

# Display Tasks (Visible to Both)
if not st.session_state.tasks:
    st.info("No active tasks right now!")
else:
    for task in st.session_state.tasks:
        t_col1, t_col2, t_col3 = st.columns([3, 1, 2])
        t_col1.write(f"**{task['title']}**")
        t_col2.write(f"🪙 {task['points']} pts")
        
        # Actions based on Status and User Role
        if task['status'] == "Completed":
            t_col3.success("✅ Done")
        else:
            if current_user == "Coco":
                if t_col3.button("Complete Task", key=f"task_{task['id']}", use_container_width=True):
                    task['status'] = "Completed"
                    st.session_state.coco_points += task['points']
                    st.toast(f"Awesome! +{task['points']} points added!")
                    st.rerun()
            else:
                t_col3.info("⏳ Pending Coco")

st.markdown("---")

# --- 6. REWARDS SHOP SECTION ---
st.header("🎁 The Rewards Vault")

# CANDY ONLY: Create Rewards
if current_user == "Candy":
    with st.expander("➕ Add a New Reward (Candy Only)", expanded=False):
        new_reward_title = st.text_input("What is the reward?")
        new_reward_cost = st.number_input("Cost (Points)", min_value=10, max_value=1000, step=10, value=100)
        if st.button("Add Reward to Shop"):
            if new_reward_title:
                new_id = len(st.session_state.rewards) + 1
                st.session_state.rewards.append({
                    "id": new_id,
                    "title": new_reward_title,
                    "cost": new_reward_cost,
                    "claimed": False
                })
                st.success(f"Added Reward: {new_reward_title}")
                st.rerun()

# Display Rewards (Visible to Both)
if not st.session_state.rewards:
    st.info("The rewards shop is currently empty.")
else:
    for reward in st.session_state.rewards:
        r_col1, r_col2, r_col3 = st.columns([3, 1, 2])
        r_col1.write(f"**{reward['title']}**")
        r_col2.write(f"🪙 {reward['cost']} pts")
        
        # Actions based on Claim Status and User Role
        if reward['claimed']:
            r_col3.warning("🎉 Claimed by Coco!")
        else:
            if current_user == "Coco":
                can_afford = st.session_state.coco_points >= reward['cost']
                if r_col3.button("Claim Reward", key=f"rew_{reward['id']}", disabled=not can_afford, use_container_width=True):
                    st.session_state.coco_points -= reward['cost']
                    reward['claimed'] = True
                    st.toast(f"Enjoy your reward: {reward['title']}!")
                    st.rerun()
            else:
                r_col3.info("🛒 Available to Claim")
