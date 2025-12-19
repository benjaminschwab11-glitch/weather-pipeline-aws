# Week 3 Plan: Data Visualization Dashboard

**Dates:** December 19-25, 2025  
**Goal:** Build and deploy interactive dashboard to visualize pipeline data

## 🎯 End State

By December 25, you will have:
- Streamlit dashboard running locally
- Dashboard deployed to Streamlit Cloud (public URL)
- Real-time weather visualizations
- 7+ days of historical trend analysis
- Demo-ready for portfolio/interviews

## 📅 Day-by-Day Breakdown

### Day 11 (Dec 19) - Local Dashboard Development
**Time:** 2 hours

**Tasks:**
- Set up Streamlit locally
- Connect to RDS from local machine
- Build current conditions display (5 cities)
- Test data refresh

**Deliverable:** Basic dashboard showing current weather

---

### Day 12 (Dec 20) - Add Visualizations
**Time:** 2 hours

**Tasks:**
- Temperature trends over time (line chart)
- Humidity comparison (box plot)
- City-by-city comparison
- Add time range selector (24h, 7d, 30d)

**Deliverable:** Interactive visualizations working locally

---

### Day 13 (Dec 21) - Data Quality Dashboard
**Time:** 1.5 hours

**Tasks:**
- Pipeline statistics display
- Data quality metrics
- Collection success rate
- Latest observation timestamp

**Deliverable:** Complete local dashboard with all features

---

### Day 14 (Dec 22) - Deploy to Streamlit Cloud
**Time:** 1.5 hours

**Tasks:**
- Create Streamlit Cloud account
- Connect GitHub repo
- Configure secrets (RDS credentials)
- Deploy dashboard
- Test public URL

**Deliverable:** Live dashboard at https://yourapp.streamlit.app

---

### Day 15 (Dec 23) - Polish & Documentation
**Time:** 1 hour

**Tasks:**
- Add dashboard README
- Update main README with dashboard link
- Create demo script
- Record 2-minute walkthrough video (optional)

**Deliverable:** Portfolio-ready presentation

---

### Day 16 (Dec 24) - Testing & Refinement
**Time:** 1 hour

**Tasks:**
- Test dashboard performance
- Fix any bugs
- Optimize query performance
- Add caching if needed

**Deliverable:** Production-quality dashboard

---

### Day 17 (Dec 25) - Week 3 Checkpoint
**Time:** 30 minutes

**Tasks:**
- Week 3 retrospective
- Demo preparation
- Plan Week 4 (advanced features or job applications)

## 🚨 Potential Blockers

1. **RDS connection from Streamlit Cloud** - May need to whitelist Streamlit IPs
2. **Query performance** - Large dataset might be slow (add caching)
3. **Streamlit Cloud limits** - Free tier has resource constraints
4. **Secrets management** - Need to configure RDS credentials securely

## 💡 Success Criteria

- [ ] Dashboard loads in under 5 seconds
- [ ] Shows data from last 7 days minimum
- [ ] Visualizations are clear and professional
- [ ] Public URL is shareable
- [ ] No errors or crashes
- [ ] Mobile-responsive (bonus)

## 📚 Resources Needed

- Streamlit documentation
- Plotly/Altair for visualizations
- Pandas for data manipulation
- psycopg2 for RDS connection

## 🎨 Dashboard Features

### Must Have
- Current weather conditions (5 cities)
- Temperature trends (line chart)
- Last 7 days of data minimum

### Nice to Have
- Humidity/pressure comparisons
- Data quality metrics
- Pipeline health status
- Time range selector

### Bonus Features
- Weather condition icons
- Dark mode toggle
- Export data to CSV
- Forecast vs actual (if time permits)

---

**Ready to build something visual. Week 3 starts tomorrow.**

