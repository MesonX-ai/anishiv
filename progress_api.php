<?php
/**
 * In-Memory Project Tracker API - AniShiv Progress Monitor
 *
 * Adapted from progress_monitory_guide.md (backend/server.php)
 * Feature Matrix:
 *   - APCu Active Memory Cache Layer (high-speed RAM threads)
 *   - JSON Transactional Disk State Fallback (crash-safe persistence)
 *
 * Endpoints (query-parameter routing so it runs on plain shared hosting):
 *   GET  progress_api.php?route=data            -> full {projects, logs} dataset
 *   POST progress_api.php?route=project         -> create a project {name, endGoal, platforms[]}
 *   POST progress_api.php?route=project_update  -> edit a project {id, name, endGoal, platforms[]}
 *   POST progress_api.php?route=log             -> add a work log {projectId, date, timeSpent, tasks, accomplishments}
 */

// Configure cross-origin browser policies for dashboard communication
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: GET, POST, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type");
header("Content-Type: application/json");

// Immediately settle browser CORS preflight check procedures
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    exit(0);
}

define('STORAGE_FILE', __DIR__ . '/projects_backup.json');

/**
 * Memory Fetch Engine
 * Resolves active state metrics from fast RAM buffer; handles transparent disk recovery fallback.
 */
function get_tracker_data() {
    // Attempt high-speed retrieval from APCu cache structures
    if (function_exists('apcu_fetch') && apcu_exists('tracker_db')) {
        return apcu_fetch('tracker_db');
    }

    // Recovery Phase: Read back snapshot data profile from file system state
    if (file_exists(STORAGE_FILE)) {
        $disk_json = @file_get_contents(STORAGE_FILE);
        $decoded = json_decode($disk_json, true);
        if (is_array($decoded)) {
            // Warm cache pool back up instantly inside system memory
            if (function_exists('apcu_store')) {
                apcu_store('tracker_db', $decoded);
            }
            return $decoded;
        }
    }

    // Default Initialization Vector
    return ['projects' => [], 'logs' => []];
}

/**
 * Memory Write & File Persist Subsystem
 * Commits active memory indexes simultaneously to the RAM cache thread and file system disk.
 */
function save_tracker_data($data) {
    if (function_exists('apcu_store')) {
        apcu_store('tracker_db', $data);
    }
    file_put_contents(STORAGE_FILE, json_encode($data, JSON_PRETTY_PRINT));
}

$route = $_GET['route'] ?? 'data';
$method = $_SERVER['REQUEST_METHOD'];
$current_db = get_tracker_data();

/**
 * ROUTE: data (GET)
 * Emits full application profile data structures to frontend state hooks.
 */
if ($route === 'data' && $method === 'GET') {
    echo json_encode($current_db);
    exit;
}

/**
 * ROUTE: project (POST)
 * Instantiates and appends a completely new tracking record object.
 */
if ($route === 'project' && $method === 'POST') {
    $input = json_decode(file_get_contents('php://input'), true);
    if (empty($input['name'])) {
        http_response_code(400);
        echo json_encode(['error' => 'Project profile must contain a valid non-empty identifier name']);
        exit;
    }

    $new_project = [
        'id' => uniqid('p_'),
        'name' => $input['name'],
        'endGoal' => $input['endGoal'] ?? '',
        'platforms' => isset($input['platforms']) && is_array($input['platforms'])
            ? array_values(array_map('strval', $input['platforms']))
            : []
    ];

    $current_db['projects'][] = $new_project;
    save_tracker_data($current_db);

    echo json_encode($new_project);
    exit;
}

/**
 * ROUTE: project_update (POST)
 * Edits an existing project profile record (name, end goal, and platform breakdown).
 */
if ($route === 'project_update' && $method === 'POST') {
    $input = json_decode(file_get_contents('php://input'), true);
    if (empty($input['id'])) {
        http_response_code(400);
        echo json_encode(['error' => 'Project profile update requires a valid project identifier ID']);
        exit;
    }

    $updated = null;
    foreach ($current_db['projects'] as &$proj) {
        if ($proj['id'] === $input['id']) {
            if (isset($input['name']) && trim($input['name']) !== '') {
                $proj['name'] = trim($input['name']);
            }
            if (array_key_exists('endGoal', $input)) {
                $proj['endGoal'] = $input['endGoal'] ?? '';
            }
            if (isset($input['platforms'])) {
                $proj['platforms'] = is_array($input['platforms'])
                    ? array_values(array_map('strval', $input['platforms']))
                    : [];
            }
            $updated = $proj;
            break;
        }
    }
    unset($proj);

    if ($updated === null) {
        http_response_code(404);
        echo json_encode(['error' => 'Project profile with the supplied ID could not be located for update']);
        exit;
    }

    save_tracker_data($current_db);
    echo json_encode($updated);
    exit;
}

/**
 * ROUTE: log (POST)
 * Appends localized operational parameters and timestamped entry blocks into active index tables.
 */
if ($route === 'log' && $method === 'POST') {
    $input = json_decode(file_get_contents('php://input'), true);
    if (empty($input['projectId']) || empty($input['date'])) {
        http_response_code(400);
        echo json_encode(['error' => 'Track execution requires valid projectId and target tracking date parameters']);
        exit;
    }

    $new_log = [
        'id' => uniqid('l_'),
        'projectId' => $input['projectId'],
        'date' => $input['date'],
        'timeSpent' => (float)($input['timeSpent'] ?? 0),
        'tasks' => $input['tasks'] ?? '',
        'accomplishments' => $input['accomplishments'] ?? ''
    ];

    $current_db['logs'][] = $new_log;
    save_tracker_data($current_db);

    echo json_encode($new_log);
    exit;
}

// Fallback error management mapping
http_response_code(404);
echo json_encode(['error' => 'Requested URI target route could not be found or executed']);
