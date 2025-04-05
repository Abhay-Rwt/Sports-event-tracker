document.addEventListener('DOMContentLoaded', function() {
    // Initialize Socket.IO
    const socket = io();
    
    // DOM elements
    const userMessageInput = document.getElementById('user-message');
    const sendBtn = document.getElementById('send-btn');
    const chatMessages = document.getElementById('chat-messages');
    const filterButtons = document.querySelectorAll('.filter-btn');
    const quickQueries = document.querySelectorAll('.quick-query');
    const eventsList = document.getElementById('events-list');
    const themeSwitch = document.getElementById('theme-switch');
    const minimizeChat = document.getElementById('minimize-chat');
    const chatSection = document.querySelector('.chat-section');
    const searchInput = document.getElementById('search-events');
    const searchBtn = document.getElementById('search-btn');
    const pageLoader = document.querySelector('.page-loader');
    const currentDate = document.getElementById('current-date');
    
    // Initialize AOS animations
    AOS.init({
        duration: 800,
        once: true,
        mirror: false
    });
    
    // Set current date
    const now = new Date();
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    currentDate.textContent = now.toLocaleDateString('en-US', options);
    
    // Check for saved theme preference
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-mode');
    }
    
    // Remove page loader after content loads
    setTimeout(() => {
        pageLoader.classList.add('hidden');
        setTimeout(() => {
            pageLoader.style.display = 'none';
        }, 500);
    }, 1000);

    // Theme toggle
    themeSwitch.addEventListener('click', function() {
        document.body.classList.toggle('dark-mode');
        const currentTheme = document.body.classList.contains('dark-mode') ? 'dark' : 'light';
        localStorage.setItem('theme', currentTheme);
    });
    
    // Minimize chat
    minimizeChat.addEventListener('click', function() {
        chatSection.classList.toggle('minimized');
        minimizeChat.querySelector('i').classList.toggle('fa-minus');
        minimizeChat.querySelector('i').classList.toggle('fa-plus');
    });

    // Event listener for search
    searchBtn.addEventListener('click', function() {
        searchEvents(searchInput.value);
    });
    
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            searchEvents(searchInput.value);
        }
    });
    
    // Function to search events
    function searchEvents(query) {
        query = query.toLowerCase().trim();
        const eventCards = document.querySelectorAll('.event-card');
        
        if (query === '') {
            eventCards.forEach(card => {
                card.style.display = 'block';
            });
            return;
        }
        
        eventCards.forEach(card => {
            const cardText = card.textContent.toLowerCase();
            if (cardText.includes(query)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    }
    
    // Event listener for send button click
    sendBtn.addEventListener('click', function() {
        sendMessage();
    });

    // Event listener for Enter key press
    userMessageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    // Event listeners for filter buttons
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all buttons
            filterButtons.forEach(btn => btn.classList.remove('active'));
            // Add active class to clicked button
            this.classList.add('active');
            // Get the sport type
            const sportType = this.getAttribute('data-type');
            // Load events based on the sport type
            loadEvents(sportType);
        });
    });

    // Event listeners for quick queries
    quickQueries.forEach(query => {
        query.addEventListener('click', function(e) {
            e.preventDefault();
            const queryText = this.textContent.trim();
            userMessageInput.value = queryText;
            sendMessage();
            
            // Apply animation to the clicked query
            this.classList.add('animate-pulse');
            setTimeout(() => {
                this.classList.remove('animate-pulse');
            }, 2000);
        });
    });

    // Function to send message
    function sendMessage() {
        const message = userMessageInput.value.trim();
        if (message) {
            // Add user message to chat
            appendMessage(message, 'user');
            // Clear input
            userMessageInput.value = '';
            // Scroll to bottom
            scrollToBottom();
            
            // Show typing indicator
            appendTypingIndicator();

            // Send message to server
            fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: message })
            })
            .then(response => response.json())
            .then(data => {
                // Remove typing indicator
                removeTypingIndicator();
                // Add bot response to chat
                appendMessage(data.response, 'bot');
                // Scroll to bottom
                scrollToBottom();
            })
            .catch(error => {
                // Remove typing indicator
                removeTypingIndicator();
                // Add error message
                appendMessage('Sorry, I encountered an error processing your request.', 'bot');
                console.error('Error:', error);
                // Scroll to bottom
                scrollToBottom();
            });
        }
    }

    // Function to append message to chat
    function appendMessage(message, sender) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', sender);
        
        // Create avatar element
        const avatarElement = document.createElement('div');
        avatarElement.classList.add('message-avatar');
        
        // Add icon based on sender
        const iconElement = document.createElement('i');
        iconElement.classList.add('fas');
        iconElement.classList.add(sender === 'user' ? 'fa-user' : 'fa-robot');
        avatarElement.appendChild(iconElement);
        
        // Create message content
        const contentElement = document.createElement('div');
        contentElement.classList.add('message-content');
        
        // Add timestamp
        const timeElement = document.createElement('div');
        timeElement.classList.add('message-time');
        const now = new Date();
        timeElement.textContent = `${now.getHours()}:${now.getMinutes().toString().padStart(2, '0')}`;
        contentElement.appendChild(timeElement);
        
        // Add message text - with Markdown rendering for bot messages
        if (sender === 'bot') {
            // Parse markdown to HTML
            const messageHTML = marked.parse(message);
            // Create a wrapper for the HTML content
            const messageContentWrapper = document.createElement('div');
            messageContentWrapper.classList.add('markdown-content');
            messageContentWrapper.innerHTML = messageHTML;
            contentElement.appendChild(messageContentWrapper);
        } else {
            // For user messages, just use text
            contentElement.appendChild(document.createTextNode(message));
        }
        
        // Append elements to message
        messageElement.appendChild(avatarElement);
        messageElement.appendChild(contentElement);
        
        // Add to chat
        chatMessages.appendChild(messageElement);
    }
    
    // Function to append typing indicator
    function appendTypingIndicator() {
        const indicatorElement = document.createElement('div');
        indicatorElement.classList.add('message', 'bot', 'typing-indicator');
        
        // Create avatar element
        const avatarElement = document.createElement('div');
        avatarElement.classList.add('message-avatar');
        
        // Add icon
        const iconElement = document.createElement('i');
        iconElement.classList.add('fas', 'fa-robot');
        avatarElement.appendChild(iconElement);
        
        // Create indicator content
        const contentElement = document.createElement('div');
        contentElement.classList.add('message-content');
        
        // Add dots
        const dotsElement = document.createElement('div');
        dotsElement.classList.add('typing-dots');
        for (let i = 0; i < 3; i++) {
            const dot = document.createElement('span');
            dot.classList.add('dot');
            dotsElement.appendChild(dot);
        }
        contentElement.appendChild(dotsElement);
        
        // Append elements to indicator
        indicatorElement.appendChild(avatarElement);
        indicatorElement.appendChild(contentElement);
        
        // Add to chat
        chatMessages.appendChild(indicatorElement);
        scrollToBottom();
    }
    
    // Function to remove typing indicator
    function removeTypingIndicator() {
        const indicator = document.querySelector('.typing-indicator');
        if (indicator) {
            indicator.remove();
        }
    }

    // Function to scroll chat to bottom
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Function to load events
    function loadEvents(type = 'all') {
        // Show loading
        eventsList.innerHTML = `<div class="loading"><i class="fas fa-spinner fa-spin"></i> Loading events...</div>`;
        
        // Fetch events from API
        fetch(`/api/sports/events?type=${type}`)
            .then(response => response.json())
            .then(data => {
                // Clear events list
                eventsList.innerHTML = '';
                
                if (data.length === 0) {
                    eventsList.innerHTML = `
                        <div class="no-events">
                            <i class="fas fa-calendar-times"></i>
                            <p>No ${type !== 'all' ? type : 'sports'} events found.</p>
                        </div>
                    `;
                    return;
                }
                
                // Add events to list with staggered animations
                data.forEach((event, index) => {
                    const eventCard = createEventCard(event);
                    eventCard.style.animationDelay = `${index * 0.1}s`;
                    eventsList.appendChild(eventCard);
                });
            })
            .catch(error => {
                eventsList.innerHTML = `
                    <div class="error">
                        <i class="fas fa-exclamation-circle"></i>
                        <p>Error loading events. Please try again.</p>
                    </div>
                `;
                console.error('Error:', error);
            });
    }

    // Function to create event card
    function createEventCard(event) {
        const eventCard = document.createElement('div');
        eventCard.classList.add('event-card', event.sport.toLowerCase());
        
        let statusClass = 'upcoming';
        if (event.status === 'LIVE') {
            statusClass = 'live';
        } else if (event.status === 'COMPLETED') {
            statusClass = 'completed';
        }
        
        // Format date
        const eventDate = new Date(event.date);
        const formattedDate = eventDate.toLocaleDateString('en-US', {
            weekday: 'short',
            month: 'short',
            day: 'numeric',
            year: 'numeric'
        });
        
        // Format time
        const formattedTime = eventDate.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit'
        });
        
        // Check if event is in 2025
        const is2025 = eventDate.getFullYear() === 2025;
        if (is2025) {
            eventCard.classList.add('future-event');
        }
        
        // Create HTML content
        eventCard.innerHTML = `
            <div class="event-status ${statusClass}">${event.status}</div>
            <div class="event-date">
                <i class="far fa-calendar-alt"></i> ${formattedDate} at ${formattedTime}
                ${is2025 ? '<span class="future-badge">2025</span>' : ''}
            </div>
            <div class="event-teams">
                <div class="team">
                    <div class="team-name">${event.home_team}</div>
                    ${event.home_score !== undefined ? `<div class="team-score">${event.home_score}</div>` : ''}
                </div>
                <div class="vs">VS</div>
                <div class="team">
                    <div class="team-name">${event.away_team}</div>
                    ${event.away_score !== undefined ? `<div class="team-score">${event.away_score}</div>` : ''}
                </div>
            </div>
            <div class="event-info">${event.competition}</div>
            <div class="event-venue"><i class="fas fa-map-marker-alt"></i> ${event.location}</div>
        `;
        
        return eventCard;
    }

    // Load events on page load
    loadEvents();
    
    // Add CSS for typing indicator
    const style = document.createElement('style');
    style.textContent = `
        .typing-dots {
            display: flex;
            gap: 4px;
        }
        
        .dot {
            width: 8px;
            height: 8px;
            background-color: var(--primary-color);
            border-radius: 50%;
            animation: dot-pulse 1.5s infinite;
            opacity: 0.6;
        }
        
        .dot:nth-child(2) {
            animation-delay: 0.2s;
        }
        
        .dot:nth-child(3) {
            animation-delay: 0.4s;
        }
        
        @keyframes dot-pulse {
            0%, 100% { transform: scale(1); opacity: 0.6; }
            50% { transform: scale(1.2); opacity: 1; }
        }
        
        .no-events, .error {
            grid-column: 1 / -1;
            text-align: center;
            padding: 40px;
            color: var(--text-color);
            opacity: 0.7;
            font-size: 16px;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 15px;
        }
        
        .no-events i, .error i {
            font-size: 36px;
            color: var(--text-color);
            opacity: 0.5;
        }
        
        .error i {
            color: var(--danger-color);
        }
    `;
    document.head.appendChild(style);
}); 