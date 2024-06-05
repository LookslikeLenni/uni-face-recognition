<script>
/* @app.get("/current/", response_model=List[UserOut])
def list_current(db: Session = Depends(get_db)): */


export default {
    data() {
        return {
            logs: [],
            intervalId: null
        };
    },
    mounted() {
        this.fetchLogs();
        this.intervalId = setInterval(this.fetchLogs, 5000);
    },
    beforeDestroy() {
        clearInterval(this.intervalId);
    },
    methods: {
        async fetchLogs() {
            try {
                const response = await fetch('http://127.0.0.1:8000/current/');
                const data = await response.json();
                console.log('Fetched logs:', data);

                // Add a timestamp to each log
                const logsWithTimestamps = data.map(log => ({
                    ...log,
                    timestamp: new Date().toLocaleString(),
                }));

                this.logs = [...this.logs, ...logsWithTimestamps].slice(-100); // Keep only the last 100 logs
            } catch (error) {
                console.error(error);
            }
        },    
        getUserImageUrl(userId, imageIndex) {
            return `http://127.0.0.1:8000/users/${userId}/images/${imageIndex}/`;
        },
    }
};
</script>

<template>
    <div>
        <h2>Current Logs</h2>
        <table class="logs">
            <thead>
                <tr>
                    <th>Picture</th>
                    <th>Name</th>
                    <th>Timestamp</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="log in logs.slice().reverse()" :key="log.id">
                    <td><img :src="getUserImageUrl(log.id, 0)" alt="User Image" class="user-image" /></td>
                    <td>{{ log.first_name }} {{ log.last_name }}</td>
                    <td>{{ log.timestamp }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>



<style scoped>
.logs {
    width: 100%;
    border-collapse: collapse;
    height: 400px;
    overflow-y: auto;
    color: #ffffff;
    
}

.logs th,
.logs td {
    padding: 8px;
    border: 1px solid #5e5e5e;
}

.logs th {
    background-color: #cccccc;
    font-weight: bold;
}

.logs img {
    width: 50px;
    height: 50px;
    object-fit: cover;
    border-radius: 50%;
}

.user-image {
    width: 69px;
    height: 69px;
    object-fit: cover; /* Ensure the image covers the specified space without stretching */
}

</style>
