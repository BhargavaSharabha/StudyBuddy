# StudyBuddy User Guide

## Feature Guides

### Creating a Study Group

1. **Access Group Creation**
   - From dashboard, click "Create Group" button
   - Or use the floating action button (+ icon)

2. **Fill Group Details**
   - **Title**: Descriptive name for your study group
   - **Subject**: Select from available academic subjects
   - **Description**: Detailed information about the group's purpose
   - **Meeting Date**: Use date picker to select meeting date
   - **Meeting Time**: Use time picker (12-hour format with AM/PM)
   - **Location**: Physical or virtual meeting location
   - **Max Members**: Set capacity (default: 8 members)

3. **Group Creation Success**
   - Automatically added as group host and member
   - Redirected to group details page
   - Group appears in your dashboard

### Joining a Study Group

#### Method 1: Browse and Join
1. **Browse Available Groups**
   - View all groups on dashboard
   - Use subject filter dropdown
   - Search by group title

2. **Select a Group**
   - Click "View Details" on any group card
   - Review group information and members

3. **Request to Join**
   - Click "Request to Join" button
   - Request sent to group host for approval
   - Status shows as "Pending"

#### Method 2: Direct Join (if space available)
- Some groups may allow immediate joining
- Click "Join Group" for instant membership

### Managing Group Requests (For Hosts)

1. **View Pending Requests**
   - Dashboard shows notification badges for pending requests
   - Navigate to group details page

2. **Review Requests**
   - See requester's profile information
   - View their subject interests

3. **Approve or Decline**
   - Click "Approve" to add member to group
   - Click "Decline" to reject request
   - Automatic notifications sent to requesters

### Group Communication

1. **Access Group Chat**
   - Navigate to group details page
   - Scroll to "Group Discussion" section

2. **Send Messages**
   - Type message in text area
   - Click "Send Message" button
   - Messages appear chronologically

3. **Message Features**
   - Real-time display of new messages
   - User attribution and timestamps
   - Available to all group members and hosts

### Editing Study Groups (Host Only)

1. **Access Edit Function**
   - Navigate to your group's details page
   - Click "Edit Group" button

2. **Modify Group Details**
   - Update any group information
   - Change meeting times or location
   - Adjust member capacity

3. **Capacity Validation**
   - Cannot reduce capacity below current member count
   - System prevents invalid configurations

### Leaving a Study Group

1. **Access Leave Option**
   - Go to group details page
   - Click "Leave Group" button

2. **Confirmation**
   - Confirm your decision to leave
   - Removed from group immediately

3. **Rejoining**
   - Can request to rejoin later
   - Must go through approval process again

### Profile Management

1. **Access Profile**
   - Click "My Profile" in navigation
   - Or visit `/profile/`

2. **Update Information**
   - Modify bio and study preferences
   - Add or remove subject interests
   - Adjust notification settings

3. **View Activity**
   - See joined groups
   - Track membership history
   - Monitor group participation

---

## Navigation Guide

### Main Navigation Bar
- **Study Buddy Logo**: Returns to dashboard
- **Find Groups**: Browse all available study groups
- **Create Group**: Start a new study group
- **My Profile**: Access profile management
- **Logout**: End current session

### Dashboard Layout

#### Filter Section
- **Subject Filter**: Dropdown to filter by academic subject
- **Search Bar**: Text search for group titles
- **Filter Button**: Apply selected filters

#### Group Cards
Each group displays:
- Group title and description
- Subject and host information
- Meeting date, time, and location
- Current member count vs. capacity
- Action buttons (View Details, Join, etc.)

#### Status Indicators
- **Green Badge**: Available to join
- **Yellow Badge**: Pending request
- **Red Badge**: Group full
- **Blue Badge**: Already a member

### Group Details Page

#### Information Section
- Complete group details
- Host and member information
- Meeting logistics

#### Action Buttons
- **Join/Request to Join**: For non-members
- **Leave Group**: For current members
- **Edit Group**: For hosts only
- **Approve/Decline**: For pending requests (hosts)

#### Discussion Section
- Message history
- Send new message form
- Real-time updates

### Mobile Navigation
- Hamburger menu for smaller screens
- Collapsible navigation items
- Touch-friendly interface elements

---

## Troubleshooting

### Common Issues and Solutions

#### Login Problems

**Issue**: Cannot log in with correct credentials
**Solutions**:
1. Ensure username/email is correct
2. Check for caps lock
3. Try password reset if forgotten
4. Clear browser cache and cookies
5. Try different browser

**Issue**: "User does not exist" error
**Solutions**:
1. Verify you've registered an account
2. Check if using correct email address
3. Try registering again if account doesn't exist

#### Group Creation Issues

**Issue**: Cannot create group - form validation errors
**Solutions**:
1. Ensure all required fields are filled
2. Check date format (MM/DD/YYYY)
3. Verify time format (HH:MM AM/PM)
4. Select a valid subject from dropdown
5. Ensure max members is a positive number

**Issue**: Date/time picker not working
**Solutions**:
1. Enable JavaScript in browser
2. Try different browser
3. Clear browser cache
4. Check for browser extensions blocking scripts

#### Group Joining Problems

**Issue**: Cannot join group - no response to click
**Solutions**:
1. Check if group is full
2. Verify you're not already a member
3. Ensure you don't have pending request
4. Refresh page and try again

**Issue**: Join request not appearing for host
**Solutions**:
1. Refresh the group details page
2. Check if request was accidentally declined
3. Verify group capacity isn't exceeded

#### Message Sending Issues

**Issue**: Messages not sending
**Solutions**:
1. Ensure you're a group member
2. Check message content isn't empty
3. Verify internet connection
4. Refresh page and try again

**Issue**: Messages not appearing
**Solutions**:
1. Refresh the page
2. Check if you're still a group member
3. Verify browser JavaScript is enabled

### Browser Compatibility

**Supported Browsers**:
- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

**Known Issues**:
- Internet Explorer not supported
- Some mobile browsers may have limited functionality
- Ad blockers may interfere with Materialize CSS

### Performance Issues

**Slow Loading**:
1. Check internet connection
2. Clear browser cache
3. Disable unnecessary browser extensions
4. Try incognito/private browsing mode

**Database Errors**:
1. Contact system administrator
2. Try again after a few minutes
3. Check if maintenance is scheduled

---

## FAQ

### General Questions

**Q: Is StudyBuddy free to use?**
A: Yes, StudyBuddy is completely free for all users.

**Q: Do I need to download any software?**
A: No, StudyBuddy runs entirely in your web browser.

**Q: Can I use StudyBuddy on my mobile device?**
A: Yes, the interface is responsive and works on mobile devices.

### Account Questions

**Q: Can I change my username after registration?**
A: Currently, usernames cannot be changed after registration. Contact support if you need assistance.

**Q: How do I delete my account?**
A: Account deletion must be requested through support. All associated data will be removed.

**Q: Can I have multiple accounts?**
A: Each user should maintain only one account per email address.

### Group Questions

**Q: How many groups can I join?**
A: There's no limit to the number of groups you can join.

**Q: Can I create multiple groups?**
A: Yes, you can host multiple study groups simultaneously.

**Q: What happens if a group host leaves?**
A: Contact support to transfer host privileges to another member.

**Q: Can I remove members from my group?**
A: Currently, members can only leave voluntarily. Contact support for assistance with problematic members.

### Privacy Questions

**Q: Who can see my profile information?**
A: Your profile is visible to other members of groups you've joined.

**Q: Are my messages private?**
A: Messages are visible to all members of the respective study group.

**Q: Can I control who can find my groups?**
A: All groups are publicly visible to registered users for discovery.

### Technical Questions

**Q: Why am I getting error messages?**
A: Check the troubleshooting section above, or contact support with specific error details.

**Q: How often is the site updated?**
A: Updates are deployed regularly with new features and bug fixes.

**Q: Is my data backed up?**
A: Yes, regular backups are maintained to protect user data.

---

## Support

### Contact Information

**Technical Support**:
- Email: support@studybuddy.com
- Response time: 24-48 hours

**Bug Reports**:
- Email: bugs@studybuddy.com
- Include: Browser version, steps to reproduce, error messages

**Feature Requests**:
- Email: features@studybuddy.com
- Describe: Desired functionality and use case

### Self-Help Resources

1. **Documentation**: This user guide and developer documentation
2. **Troubleshooting**: Common issues and solutions section
3. **FAQ**: Frequently asked questions
4. **Community**: User forums (if available)

### Reporting Issues

When reporting issues, please include:
1. **Browser and version**
2. **Operating system**
3. **Steps to reproduce the problem**
4. **Expected vs. actual behavior**
5. **Screenshots (if applicable)**
6. **Error messages (exact text)**

### Emergency Contact

For urgent issues affecting multiple users:
- Emergency hotline: [To be configured]
- Available: 24/7 for critical issues

---

*Last updated: [Current Date]*
*Version: 1.0* 