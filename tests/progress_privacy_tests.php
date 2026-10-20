<?php
/**
 * Deterministic isolated tests; never connect to a WordPress instance.
 * Run: php tests/progress_privacy_tests.php
 */
error_reporting(E_ALL);
define('ABSPATH',__DIR__.'/../');
define('ARRAY_A','ARRAY_A');
define('DAY_IN_SECONDS',86400);
$GLOBALS['mnin_fixture_uid']=77;
$GLOBALS['mnin_logged_in']=false;
$GLOBALS['mnin_allowed']=false;
$GLOBALS['mnin_user_meta']=array(
 '_mnin_student_access'=>'3ac',
 '_mnin_student_state_v1'=>array('completed'=>array('m1')),
 '_mnin_pixel_goal_v1'=>array('title'=>'Objectif test','steps'=>array(array('done'=>true),array('done'=>false))),
 '_mnin_pixel_goal_history_v1'=>array(array('title'=>'Ancien objectif')),
 '_mnin_journey_v1'=>array('steps'=>array(array('done'=>true),array('done'=>false),array('done'=>false))),
 'mnin_atelier_attempts_v1'=>array(11=>array('correct'=>true),12=>array('correct'=>false)),
 '_mnin_suite_journal'=>array('Protected by existing exporter'),
);
$GLOBALS['mnin_hooks']=array();
function add_filter($hook,$callback,...$args){$GLOBALS['mnin_hooks'][$hook][]=$callback;return true;}
function add_action($hook,$callback,...$args){$GLOBALS['mnin_hooks'][$hook][]=$callback;return true;}
function register_activation_hook(...$args){return true;}
function is_user_logged_in(){return $GLOBALS['mnin_logged_in'];}
function get_current_user_id(){return $GLOBALS['mnin_fixture_uid'];}
function current_user_can($cap){return false;}
function mnin_student_access(){return $GLOBALS['mnin_allowed'];}
function mnin_student_activities(){return array(array('key'=>'m1'),array('key'=>'m2'));}
function get_user_meta($uid,$key,$single=true){return array_key_exists($key,$GLOBALS['mnin_user_meta'])?$GLOBALS['mnin_user_meta'][$key]:'';}
function metadata_exists($type,$uid,$key){return array_key_exists($key,$GLOBALS['mnin_user_meta']);}
function delete_user_meta($uid,$key){unset($GLOBALS['mnin_user_meta'][$key]);return true;}
function get_user_by($field,$value){return $field==='email'&&$value==='student@example.test'?(object)array('ID'=>77):false;}
function is_email($email){return (bool)filter_var($email,FILTER_VALIDATE_EMAIL);}
function wp_json_encode($value,$flags=0){return json_encode($value,$flags);}
class WP_Error {public $code;public function __construct($code='',$message='',$data=null){$this->code=$code;}}
class FakeWpdb {
 public $prefix='wp_';
 public function prepare($query,...$args){return $query;}
 public function get_results($query,$output=null){return array();}
 public function get_col($query){return array();}
 public function get_var($query){return 0;}
}
$GLOBALS['wpdb']=new FakeWpdb();
require __DIR__.'/../wordpress/plugins/mnin-progress-quality/mnin-progress-quality.php';
function expect($condition,$what){if(!$condition){fwrite(STDERR,"FAIL ".$what.PHP_EOL);exit(1);}echo "PASS ".$what.PHP_EOL;}
expect(isset($GLOBALS['mnin_hooks']['wp_privacy_personal_data_exporters']),'privacy exporter hook registered');
expect(isset($GLOBALS['mnin_hooks']['wp_privacy_personal_data_erasers']),'privacy eraser hook registered');
$anonymous=MNIN_Progress_Quality::overview();
expect($anonymous instanceof WP_Error,'anonymous overview denied');
$GLOBALS['mnin_logged_in']=true;
$other=MNIN_Progress_Quality::overview();
expect($other instanceof WP_Error,'non-3AC overview denied');
$GLOBALS['mnin_allowed']=true;
$overview=MNIN_Progress_Quality::overview();
expect($overview['overall_percent']===null&&$overview['read_only']===true,'no synthetic global percent');
expect($overview['lessons']['completed']===1&&$overview['lessons']['available']===2&&$overview['lessons']['percent']===50,'legacy lessons use own denominator');
expect($overview['primary_goal']['percent']===50,'Pixel + Learning share primary goal');
expect($overview['student_journey']['percent']===33&&$overview['student_journey']['merged_with_primary_goal']===false,'Journey separate from primary goal');
expect($overview['interactive_quiz']['last_attempts_recorded']===2&&$overview['interactive_quiz']['last_answers_correct']===1,'QCM last attempts are not added to learning stats');
$export=MNIN_Progress_Quality::export_other_personal_data('student@example.test');
expect(count($export['data'])===1&&count($export['data'][0]['data'])===5,'all five additional personal-data stores exported');
$none=MNIN_Progress_Quality::export_other_personal_data('other@example.test');
expect(!$none['data'],'unrelated email has no student data');
$erase=MNIN_Progress_Quality::erase_other_personal_data('student@example.test');
expect($erase['items_removed']===true&&!$erase['items_retained'],'five additional stores erased');
expect($GLOBALS['mnin_user_meta']['_mnin_student_access']==='3ac','3AC access not deleted');
expect(isset($GLOBALS['mnin_user_meta']['_mnin_suite_journal']),'existing journal unchanged (handled by original eraser)');
expect(!MNIN_Progress_Quality::export_other_personal_data('student@example.test')['data'],'erased stores are no longer exported');
echo "ALL UNIT TESTS PASSED (mocked WordPress environment).".PHP_EOL;
