<?php
/**
 * Plugin Name: MNIN NBDA — Progress & Quality
 * Description: Progression vérifiable, contrôles de qualité et instantanés ciblés des pages MNIN.
 * Version: 1.0.3
 * Requires at least: 6.6
 * Requires PHP: 7.4
 * Author: MNIN NBDA
 * License: GPL-2.0-or-later
 */
defined('ABSPATH') || exit;
final class MNIN_Progress_Quality {
    const VERSION='1.0.3';
    const DB_VERSION='1.0.0';
    public static function install(){
        global $wpdb;require_once ABSPATH.'wp-admin/includes/upgrade.php';$charset=$wpdb->get_charset_collate();
        dbDelta("CREATE TABLE {$wpdb->prefix}mnin_suite_events (
 id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
 user_id bigint(20) unsigned NOT NULL,
 event_key varchar(150) NOT NULL,
 kind varchar(24) NOT NULL,
 occurred_at datetime NOT NULL,
 PRIMARY KEY  (id),
 UNIQUE KEY user_event (user_id,event_key),
 KEY user_kind (user_id,kind)
) $charset;");
        dbDelta("CREATE TABLE {$wpdb->prefix}mnin_suite_attempts (
 id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
 user_id bigint(20) unsigned NOT NULL,
 activity varchar(80) NOT NULL,
 attempts int unsigned NOT NULL DEFAULT 0,
 successes int unsigned NOT NULL DEFAULT 0,
 last_correct tinyint NOT NULL DEFAULT 0,
 last_at datetime NOT NULL,
 due_at datetime NOT NULL,
 PRIMARY KEY  (id),
 UNIQUE KEY user_activity (user_id,activity)
) $charset;");
        update_option('mnin_suite_db_version',self::DB_VERSION,false);
    }
    public static function allowed(){
        if(!is_user_logged_in())return false;
        if(current_user_can('manage_options'))return true;
        return function_exists('mnin_student_access') ? mnin_student_access() : '3ac'===get_user_meta(get_current_user_id(),'_mnin_student_access',true);
    }
    public static function permission(){return self::allowed()?true:new WP_Error('mnin_forbidden','Connexion et accès élève nécessaires.',array('status'=>is_user_logged_in()?403:401));}
    public static function event($key,$kind){
        global $wpdb;if(!self::allowed()||!in_array($kind,array('activity','goal'),true))return false;
        return false!==$wpdb->query($wpdb->prepare("INSERT IGNORE INTO {$wpdb->prefix}mnin_suite_events (user_id,event_key,kind,occurred_at) VALUES (%d,%s,%s,%s)",get_current_user_id(),substr(sanitize_key($key),0,150),$kind,current_time('mysql',true)));
    }
    public static function attempt($id,$correct){
        global $wpdb;if(!self::allowed())return false;$uid=get_current_user_id();
        $previous=$wpdb->get_row($wpdb->prepare("SELECT successes FROM {$wpdb->prefix}mnin_suite_attempts WHERE user_id=%d AND activity=%s",$uid,$id),ARRAY_A);
        $successes=$previous?(int)$previous['successes']:0;
        $days=$correct?array(1,3,7,14)[min(3,$successes)]:1;
        $now=gmdate('Y-m-d H:i:s');$due=gmdate('Y-m-d H:i:s',time()+DAY_IN_SECONDS*$days);
        $result=$wpdb->query($wpdb->prepare("INSERT INTO {$wpdb->prefix}mnin_suite_attempts (user_id,activity,attempts,successes,last_correct,last_at,due_at) VALUES (%d,%s,1,%d,%d,%s,%s) ON DUPLICATE KEY UPDATE attempts=attempts+1, successes=successes+VALUES(successes), last_correct=VALUES(last_correct),last_at=VALUES(last_at),due_at=VALUES(due_at)",$uid,$id,$correct?1:0,$correct?1:0,$now,$due));
        if(false===$result)return false;
        return !$correct||self::event('activity-'.$id,'activity');
    }
    public static function summary(){
        global $wpdb;$uid=get_current_user_id();
        if(!self::allowed())return array('activities_completed'=>0,'goals_reached'=>0,'mastery_percent'=>null,'available_activities'=>0,'attempts'=>0,'reviews_due'=>0,'formulas'=>array());
        $catalog=class_exists('MNIN_Learning_Experience')?MNIN_Learning_Experience::catalog():array();
        $rows=$wpdb->get_results($wpdb->prepare("SELECT activity,attempts,last_correct,due_at FROM {$wpdb->prefix}mnin_suite_attempts WHERE user_id=%d",$uid),ARRAY_A);
        $events=$wpdb->get_col($wpdb->prepare("SELECT event_key FROM {$wpdb->prefix}mnin_suite_events WHERE user_id=%d AND kind='activity'",$uid));
        $done=0;$attempts=0;$due=0;
        foreach($catalog as $id=>$activity){if(in_array('activity-'.$id,$events,true))$done++;}
        foreach($rows as $r){if(!isset($catalog[$r['activity']]))continue;$attempts+=(int)$r['attempts'];if($r['due_at']<=gmdate('Y-m-d H:i:s'))$due++;}
        $goal_count=(int)$wpdb->get_var($wpdb->prepare("SELECT COUNT(*) FROM {$wpdb->prefix}mnin_suite_events WHERE user_id=%d AND kind='goal'",$uid));
        return array('activities_completed'=>$done,'available_activities'=>count($catalog),'goals_reached'=>$goal_count,'mastery_percent'=>$catalog?(int)floor(100*$done/count($catalog)):null,'attempts'=>$attempts,'reviews_due'=>$due,'formulas'=>array('activities'=>'Nombre d’activités distinctes réussies dans l’atelier.','mastery'=>'Activités distinctes réussies ÷ activités proposées dans l’atelier × 100. Ce chiffre ne mesure pas la maîtrise de tout le programme.','goals'=>'Objectifs personnels distincts dont toutes les étapes ont été déclarées terminées.','reviews'=>'Activités tentées dont la prochaine révision est arrivée : 1, 3, 7 puis 14 jours après une bonne réponse ; 1 jour après une erreur.'));
    }
    public static function reviews(){global $wpdb;if(!self::allowed())return array();return $wpdb->get_results($wpdb->prepare("SELECT activity,attempts,last_correct,due_at FROM {$wpdb->prefix}mnin_suite_attempts WHERE user_id=%d ORDER BY due_at ASC LIMIT 40",get_current_user_id()),ARRAY_A);}
    public static function erase($uid){global $wpdb;foreach(array('events','attempts') as $table)$wpdb->delete($wpdb->prefix.'mnin_suite_'.$table,array('user_id'=>absint($uid)),array('%d'));delete_user_meta($uid,'_mnin_suite_journal');}

    /**
     * Récapitulatif strictement personnel. Chaque indicateur conserve son propre
     * dénominateur : aucun pourcentage global fictif ni migration automatique.
     */
    public static function overview(){
        if (!self::allowed()) return new WP_Error('mnin_forbidden','Accès réservé à votre compte élève.',array('status'=>is_user_logged_in()?403:401));
        $uid=get_current_user_id();
        $legacy=get_user_meta($uid,'_mnin_student_state_v1',true);
        $done_keys=is_array($legacy)&&isset($legacy['completed'])&&is_array($legacy['completed']) ? array_values(array_unique(array_filter($legacy['completed'],'is_string'))) : array();
        $catalog=function_exists('mnin_student_activities') ? mnin_student_activities() : array();
        $lesson_keys=array();
        foreach((array)$catalog as $row) if(is_array($row)&&isset($row['key'])&&is_string($row['key'])) $lesson_keys[$row['key']]=true;
        $total_lessons=count($lesson_keys);
        $done_lessons=count(array_intersect(array_keys($lesson_keys),$done_keys));

        $goal=get_user_meta($uid,'_mnin_pixel_goal_v1',true);
        $goal_steps=is_array($goal)&&isset($goal['steps'])&&is_array($goal['steps'])?$goal['steps']:array();
        $goal_done=0;foreach($goal_steps as $step)if(is_array($step)&&!empty($step['done']))$goal_done++;
        $journey=get_user_meta($uid,'_mnin_journey_v1',true);
        $journey_steps=is_array($journey)&&isset($journey['steps'])&&is_array($journey['steps'])?$journey['steps']:array();
        $journey_done=0;foreach($journey_steps as $step)if(is_array($step)&&!empty($step['done']))$journey_done++;
        $quiz=get_user_meta($uid,'mnin_atelier_attempts_v1',true);
        $quiz_attempts=0;$quiz_correct=0;
        if(is_array($quiz))foreach($quiz as $item){if(!is_array($item))continue;$quiz_attempts++;if(!empty($item['correct']))$quiz_correct++;}

        return array(
            'overall_percent'=>null,
            'reason'=>'Sources distinctes ; aucune moyenne ou fusion implicite.',
            'lessons'=>array('source'=>'_mnin_student_state_v1','completed'=>$done_lessons,'available'=>$total_lessons,'percent'=>$total_lessons?(int)floor(100*$done_lessons/$total_lessons):null),
            'primary_goal'=>array('source'=>'_mnin_pixel_goal_v1','completed_steps'=>$goal_done,'steps'=>count($goal_steps),'percent'=>$goal_steps?(int)floor(100*$goal_done/count($goal_steps)):null),
            'student_journey'=>array('source'=>'_mnin_journey_v1','completed_steps'=>$journey_done,'steps'=>count($journey_steps),'percent'=>$journey_steps?(int)floor(100*$journey_done/count($journey_steps)):null,'merged_with_primary_goal'=>false),
            'interactive_quiz'=>array('source'=>'mnin_atelier_attempts_v1','last_attempts_recorded'=>$quiz_attempts,'last_answers_correct'=>$quiz_correct,'percent'=>null,'note'=>'Chaque QCM conserve seulement son dernier résultat.'),
            'learning_experience'=>self::summary(),
            'read_only'=>true,
        );
    }

    /** Magasins complémentaires ; le carnet et les deux tables SQL ont leur eraser existant. */
    private static function other_personal_stores(){
        return array(
            '_mnin_student_state_v1'=>'Leçons et avancement 3AC',
            '_mnin_pixel_goal_v1'=>'Objectif personnel Pixel Studio et Learning Experience',
            '_mnin_pixel_goal_history_v1'=>'Historique des objectifs Pixel Studio',
            '_mnin_journey_v1'=>'Objectifs Student Journey',
            'mnin_atelier_attempts_v1'=>'Derniers résultats des QCM interactifs',
        );
    }
    public static function export_other_personal_data($email,$page=1){
        $out=array('data'=>array(),'done'=>true);
        if(1!==(int)$page||!is_string($email)||!is_email($email))return $out;
        $user=get_user_by('email',$email);if(!$user)return $out;
        $data=array();
        foreach(self::other_personal_stores() as $key=>$label){
            if(!metadata_exists('user',$user->ID,$key))continue;
            $raw=get_user_meta($user->ID,$key,true);
            $json=wp_json_encode($raw,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);
            $data[]=array('name'=>$label,'value'=>false===$json?'(valeur non exportable)':$json);
        }
        if($data)$out['data'][]=array('group_id'=>'mnin-additional-learning','group_label'=>'MNIN — données complémentaires élève','item_id'=>'mnin-additional-learning-'.$user->ID,'data'=>$data);
        return $out;
    }
    public static function erase_other_personal_data($email,$page=1){
        $out=array('items_removed'=>false,'items_retained'=>false,'messages'=>array(),'done'=>true);
        if(1!==(int)$page||!is_string($email)||!is_email($email))return $out;
        $user=get_user_by('email',$email);if(!$user)return $out;
        foreach(self::other_personal_stores() as $key=>$label){
            if(!metadata_exists('user',$user->ID,$key))continue;
            delete_user_meta($user->ID,$key);
            if(metadata_exists('user',$user->ID,$key)){
                $out['items_retained']=true;
                $out['messages'][]='Échec de suppression : '.$label;
            }else $out['items_removed']=true;
        }
        // Le compte, les droits d'accès 3AC et le catalogue de cours restent inchangés.
        return $out;
    }

    public static function boot(){
        add_filter('wp_privacy_personal_data_exporters',function($list){
            $list['mnin-additional-learning']=array('exporter_friendly_name'=>'MNIN — autres données élèves','callback'=>array(__CLASS__,'export_other_personal_data'));return $list;
        });
        add_filter('wp_privacy_personal_data_erasers',function($list){
            $list['mnin-additional-learning']=array('eraser_friendly_name'=>'MNIN — autres données élèves','callback'=>array(__CLASS__,'erase_other_personal_data'));return $list;
        });
        add_action('rest_api_init',function(){
            register_rest_route('mnin-progress/v1','/overview',array(
                'methods'=>'GET','permission_callback'=>array(__CLASS__,'permission'),
                'callback'=>function(){return rest_ensure_response(self::overview());},
            ));
        });

        add_filter('rest_post_dispatch',function($response,$server,$request){if(0===strpos($request->get_route(),'/mnin-learning/')||0===strpos($request->get_route(),'/mnin-progress/')){$response->header('Cache-Control','private, no-store, max-age=0');$response->header('X-Robots-Tag','noindex, nofollow');}return $response;},10,3);
        add_action('admin_menu',function(){add_menu_page('MNIN Progress & Quality','MNIN Qualité','manage_options','mnin-quality',array(__CLASS__,'admin'),'dashicons-shield',60);});
        add_action('admin_post_mnin_quality_snapshot',array(__CLASS__,'snapshot_action'));
        add_action('rest_api_init',function(){register_rest_route('mnin-progress/v1','/summary',array('methods'=>'GET','callback'=>function(){return rest_ensure_response(self::summary());},'permission_callback'=>array(__CLASS__,'permission')));});
        add_filter('wp_privacy_personal_data_exporters',function($list){$list['mnin-suite']=array('exporter_friendly_name'=>'MNIN atelier et progression','callback'=>array(__CLASS__,'exporter'));return $list;});
        add_filter('wp_privacy_personal_data_erasers',function($list){$list['mnin-suite']=array('eraser_friendly_name'=>'MNIN atelier et progression','callback'=>array(__CLASS__,'eraser'));return $list;});
    }
    public static function exporter($email,$page=1){
        global $wpdb;$u=get_user_by('email',$email);$data=array();
        if($u&&1===(int)$page){$values=array('Événements'=>$wpdb->get_results($wpdb->prepare("SELECT event_key,kind,occurred_at FROM {$wpdb->prefix}mnin_suite_events WHERE user_id=%d",$u->ID),ARRAY_A),'Tentatives'=>$wpdb->get_results($wpdb->prepare("SELECT activity,attempts,successes,last_correct,last_at,due_at FROM {$wpdb->prefix}mnin_suite_attempts WHERE user_id=%d",$u->ID),ARRAY_A),'Carnet'=>get_user_meta($u->ID,'_mnin_suite_journal',true));$items=array();foreach($values as $name=>$value)$items[]=array('name'=>$name,'value'=>wp_json_encode($value,JSON_UNESCAPED_UNICODE));$data[]=array('group_id'=>'mnin-suite','group_label'=>'MNIN atelier','item_id'=>'mnin-suite-'.$u->ID,'data'=>$items);}
        return array('data'=>$data,'done'=>true);
    }
    public static function eraser($email,$page=1){$u=get_user_by('email',$email);if($u)self::erase($u->ID);return array('items_removed'=>(bool)$u,'items_retained'=>false,'messages'=>array('Les objectifs Pixel Studio appartiennent à son propre suivi et restent conservés.'),'done'=>true);}
    public static function snapshots($id){$v=get_post_meta($id,'_mnin_quality_snapshots',true);return is_array($v)?$v:array();}
    public static function page_hash($p){return hash('sha256',wp_json_encode(array($p->post_title,$p->post_content)));}
    public static function capture($id){$p=get_post($id);if(!current_user_can('manage_options')||!$p||'page'!==$p->post_type)return new WP_Error('forbidden','Page inaccessible.');$list=self::snapshots($id);$list[]=array('date'=>gmdate('c'),'title'=>$p->post_title,'content'=>$p->post_content,'reason'=>'Instantané manuel');return update_post_meta($id,'_mnin_quality_snapshots',array_slice($list,-10));}
    public static function restore($id,$index,$expected_hash){$p=get_post($id);$list=self::snapshots($id);if(!current_user_can('manage_options')||!$p||'page'!==$p->post_type)return new WP_Error('forbidden','Page inaccessible.');if(!isset($list[$index])||!is_string($expected_hash)||!hash_equals(self::page_hash($p),$expected_hash))return new WP_Error('conflict','La page a changé ou l’instantané est absent.',array('status'=>409));$saved=$list[$index];$list[]=array('date'=>gmdate('c'),'title'=>$p->post_title,'content'=>$p->post_content,'reason'=>'Avant restauration');if(!update_post_meta($id,'_mnin_quality_snapshots',array_slice($list,-10)))return new WP_Error('snapshot','Impossible de conserver le contenu actuel.');return wp_update_post(array('ID'=>$id,'post_content'=>wp_slash($saved['content']),'post_title'=>wp_slash($saved['title'])),true);}
    public static function snapshot_action(){
        if(!current_user_can('manage_options'))wp_die('Action non autorisée.',403);check_admin_referer('mnin_quality_snapshot');
        $id=isset($_POST['page_id'])?absint($_POST['page_id']):0;$p=get_post($id);
        if(!$p||'page'!==$p->post_type||!current_user_can('edit_post',$id))wp_die('Page invalide.',400);
        $mode=isset($_POST['mode'])?sanitize_key($_POST['mode']):'snapshot';
        if('restore'===$mode){
            $index=isset($_POST['snapshot'])?absint($_POST['snapshot']):999;$hash=isset($_POST['expected_hash'])?sanitize_text_field(wp_unslash($_POST['expected_hash'])):'';
            $result=self::restore($id,$index,$hash);if(is_wp_error($result))wp_die(esc_html($result->get_error_message()));
        }else{$result=self::capture($id);if(!$result)wp_die('Impossible d’enregistrer l’instantané.');}
        wp_safe_redirect(add_query_arg(array('page'=>'mnin-quality','page_id'=>$id,'saved'=>1),admin_url('admin.php')));exit;
    }
    public static function admin(){
        if(!current_user_can('manage_options'))return;$id=isset($_GET['page_id'])?absint($_GET['page_id']):344;$p=get_post($id);$list=$p?self::snapshots($id):array();
        echo '<div class="wrap"><h1>MNIN Progress & Quality</h1><p>Calculs réels · restauration ciblée · version '.esc_html(self::VERSION).'</p>';
        echo '<h2>État des modules</h2><table class="widefat striped"><tbody>';foreach(array('Base de progression'=>get_option('mnin_suite_db_version')===self::DB_VERSION,'Atelier élève'=>class_exists('MNIN_Learning_Experience'),'Design Studio'=>class_exists('MNIN_Design_Studio'),'Pixel Studio'=>class_exists('MNIN_Pixel_Studio')) as $name=>$ok)echo '<tr><td>'.esc_html($name).'</td><td>'.($ok?'Disponible':'Non disponible').'</td></tr>';echo '</tbody></table>';
        echo '<h2>Instantanés des pages</h2><p>Contenu et titre uniquement. Les comptes, médias, réglages et fichiers du thème ne sont pas sauvegardés par cet outil.</p><form method="get"><input type="hidden" name="page" value="mnin-quality"><label>ID de la page <input type="number" name="page_id" min="1" value="'.esc_attr($id).'"></label> <button class="button">Charger la page</button></form>';
        if($p&&'page'===$p->post_type){echo '<h3>'.esc_html($p->post_title).'</h3><form method="post" action="'.esc_url(admin_url('admin-post.php')).'">';wp_nonce_field('mnin_quality_snapshot');echo '<input type="hidden" name="action" value="mnin_quality_snapshot"><input type="hidden" name="page_id" value="'.esc_attr($id).'"><button class="button button-primary" name="mode" value="snapshot">Créer un instantané</button></form>';
            foreach(array_reverse($list,true) as $index=>$item){echo '<form style="margin-top:12px" method="post" action="'.esc_url(admin_url('admin-post.php')).'">';wp_nonce_field('mnin_quality_snapshot');echo '<input type="hidden" name="action" value="mnin_quality_snapshot"><input type="hidden" name="mode" value="restore"><input type="hidden" name="page_id" value="'.esc_attr($id).'"><input type="hidden" name="snapshot" value="'.esc_attr($index).'"><input type="hidden" name="expected_hash" value="'.esc_attr(self::page_hash($p)).'"><span>'.esc_html($item['date'].' — '.$item['reason']).'</span> <button class="button">Restaurer ce contenu</button></form>';}}
        echo '<h2>Formules et confidentialité</h2><p>Les exercices sont corrigés côté serveur. Une activité et un objectif distincts ne comptent qu’une fois. Les étapes personnelles restent auto-déclarées. Les données sont exportables et effaçables dans Outils → Exporter / Effacer les données.</p><p>Aucun suivi de navigation, aucune API externe, aucune collecte du temps passé.</p></div>';
    }
}
register_activation_hook(__FILE__,array('MNIN_Progress_Quality','install'));
MNIN_Progress_Quality::boot();
require_once __DIR__.'/reception.php';

