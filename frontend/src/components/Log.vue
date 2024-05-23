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
        this.intervalId = setInterval(this.fetchLogs, 100000);
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
                this.logs = data;
            } catch (error) {
                console.error(error);
            }
        }
    }
};
</script>

<template>
    <div>
        <h2>Current Logs</h2>
        <ul>
            <li v-for="log in logs" :key="log.id">
                <p>{{ log.timestamp }}: {{ log.message }}</p>
            </li>
        </ul>
    </div>
</template>